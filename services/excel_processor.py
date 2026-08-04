import json
import os

import openpyxl
from sqlalchemy.orm import Session

from models import DifficultyLevel, ExcelQuestion, Question, QuestionType


FULL_HEADERS = [
    "id", "subject_code", "subject_unit", "content", "code_snippet",
    "difficulty", "benchmark_time", "option_1", "option_2", "option_3",
    "option_4", "correct_option", "explanation", "tags", "is_required",
]
FULL_HEADERS_V1 = FULL_HEADERS[:-1]
LEGACY_HEADERS = [
    "title", "content", "difficulty", "correct_answer", "explanation",
    "options", "tags",
]


def _text(value, *, required=False):
    if value is None:
        if required:
            raise ValueError("필수값이 비어 있습니다")
        return None
    result = str(value).strip()
    if required and not result:
        raise ValueError("필수값이 비어 있습니다")
    return result or None


def _integer(value, field_name, *, minimum=None, maximum=None):
    if value is None or str(value).strip() == "":
        raise ValueError(f"{field_name} 값이 비어 있습니다")
    try:
        number = int(value)
    except (TypeError, ValueError):
        raise ValueError(f"{field_name}은(는) 정수여야 합니다")
    if minimum is not None and number < minimum:
        raise ValueError(f"{field_name}은(는) {minimum} 이상이어야 합니다")
    if maximum is not None and number > maximum:
        raise ValueError(f"{field_name}은(는) {maximum} 이하여야 합니다")
    return number


def _difficulty(value):
    name = _text(value, required=True).upper()
    try:
        return DifficultyLevel[name]
    except KeyError:
        allowed = ", ".join(level.name for level in DifficultyLevel)
        raise ValueError(f"difficulty는 {allowed} 중 하나여야 합니다")


def _boolean(value, field_name, *, default=False):
    if value is None or str(value).strip() == "":
        return default
    if isinstance(value, bool):
        return value
    normalized = str(value).strip().lower()
    if normalized in {"true", "1", "yes", "y", "필수"}:
        return True
    if normalized in {"false", "0", "no", "n", "일반"}:
        return False
    raise ValueError(f"{field_name}은(는) TRUE 또는 FALSE여야 합니다")


def _full_question(row, subject_id, source_file):
    external_id = _integer(row["id"], "id", minimum=1)
    correct_option = _integer(row["correct_option"], "correct_option", minimum=1, maximum=4)
    benchmark_time = _integer(row["benchmark_time"], "benchmark_time", minimum=1)
    options = [_text(row[f"option_{index}"], required=True) for index in range(1, 5)]
    subject_unit = _text(row["subject_unit"], required=True)

    return Question(
        subject_id=subject_id,
        question_type=QuestionType.EXCEL,
        title=subject_unit,
        content=_text(row["content"], required=True),
        correct_answer=str(correct_option - 1),
        explanation=_text(row["explanation"]),
        difficulty=_difficulty(row["difficulty"]),
        source_file=source_file,
        options=json.dumps(options, ensure_ascii=False),
        tags=_text(row["tags"]),
        external_id=external_id,
        subject_code=_text(row["subject_code"], required=True).upper(),
        subject_unit=subject_unit,
        code_snippet=_text(row["code_snippet"]),
        benchmark_time=benchmark_time,
        correct_option=correct_option,
        is_required=_boolean(row.get("is_required"), "is_required"),
    )


def _legacy_question(row, subject_id, source_file):
    return Question(
        subject_id=subject_id,
        question_type=QuestionType.EXCEL,
        title=_text(row["title"], required=True),
        content=_text(row["content"], required=True),
        correct_answer=_text(row["correct_answer"]),
        explanation=_text(row["explanation"]),
        difficulty=_difficulty(row["difficulty"]),
        source_file=source_file,
        options=_text(row["options"]),
        tags=_text(row["tags"]),
    )


async def process_excel_file(file_path: str, subject_id: int, db: Session) -> dict:
    """14컬럼 표준 Excel 또는 기존 7컬럼 Excel을 문제 테이블에 등록한다."""
    try:
        workbook = openpyxl.load_workbook(file_path, read_only=True, data_only=True)
        sheet = workbook["문제등록"] if "문제등록" in workbook.sheetnames else workbook.active
        headers = [_text(cell.value) for cell in sheet[1]]

        if headers in (FULL_HEADERS, FULL_HEADERS_V1):
            question_factory = _full_question
        elif headers == LEGACY_HEADERS:
            question_factory = _legacy_question
        else:
            workbook.close()
            return {
                "success": False, "count": 0,
                "message": "Excel 헤더 형식이 올바르지 않습니다.",
                "errors": [f"필요한 헤더: {', '.join(FULL_HEADERS)}"],
            }

        created = 0
        errors = []
        seen_external_ids = set()
        source_file = os.path.basename(file_path)

        for row_number, values in enumerate(
            sheet.iter_rows(min_row=2, max_col=len(headers), values_only=True), start=2
        ):
            if all(value is None or str(value).strip() == "" for value in values):
                continue
            row = dict(zip(headers, values))
            try:
                question = question_factory(row, subject_id, source_file)
                if question.external_id is not None:
                    if question.external_id in seen_external_ids:
                        raise ValueError(f"id {question.external_id}가 파일 안에서 중복되었습니다")
                    seen_external_ids.add(question.external_id)
                db.add(question)
                db.flush()
                db.add(ExcelQuestion(
                    question_id=question.id,
                    excel_row_number=row_number,
                    file_name=source_file,
                ))
                created += 1
            except Exception as exc:
                errors.append(f"{row_number}행: {exc}")

        workbook.close()
        if errors:
            db.rollback()
            return {
                "success": False, "count": 0,
                "message": f"등록하지 못했습니다. {len(errors)}개 행을 확인하세요.",
                "errors": errors,
            }
        if created == 0:
            db.rollback()
            return {
                "success": False, "count": 0,
                "message": "등록할 문제 데이터가 없습니다.",
                "errors": ["문제등록 시트의 2행부터 데이터를 입력하세요."],
            }

        db.commit()
        return {
            "success": True, "count": created,
            "message": f"{created}개 문제를 성공적으로 등록했습니다.",
            "errors": [],
        }
    except Exception as exc:
        db.rollback()
        return {
            "success": False, "count": 0,
            "message": f"Excel 처리 중 오류가 발생했습니다: {exc}",
            "errors": [str(exc)],
        }
