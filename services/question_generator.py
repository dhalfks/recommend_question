from openai import AsyncOpenAI
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
import json

from config import settings
from models import DifficultyLevel, Question, QuestionType

client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY) if settings.OPENAI_API_KEY else None


class GeneratedQuestion(BaseModel):
    title: str = Field(min_length=1, max_length=255)
    content: str = Field(min_length=1)
    difficulty: DifficultyLevel
    options: list[str] = Field(min_length=4, max_length=4)
    correct_option: int = Field(ge=0, le=3)
    explanation: str = Field(min_length=1)


class GeneratedQuestionSet(BaseModel):
    questions: list[GeneratedQuestion] = Field(min_length=1, max_length=5)


def serialize_question(question: Question) -> dict:
    return {
        "id": question.id,
        "title": question.title,
        "content": question.content,
        "difficulty": question.difficulty.value,
        "options": json.loads(question.options or "[]"),
        "correct_option": question.correct_option,
        "correct_answer": question.correct_answer,
        "explanation": question.explanation,
        "source_file": question.source_file,
        "is_required": question.is_required,
    }


def _response_usage(response) -> dict:
    usage = getattr(response, "usage", None)
    return {
        "input_tokens": getattr(usage, "input_tokens", None),
        "output_tokens": getattr(usage, "output_tokens", None),
    }


async def generate_questions_from_code(
    code_content: str,
    file_name: str,
    subject_id: int,
    file_type: str,
    db: Session,
    professor_id: int | None = None,
) -> dict:
    """Analyze an uploaded text/code file and persist validated quiz questions."""
    if not client:
        return {"success": False, "count": 0, "questions": [], "message": "OPENAI_API_KEY가 설정되지 않았습니다."}
    if not code_content.strip():
        return {"success": False, "count": 0, "questions": [], "message": "파일 내용이 비어 있습니다."}

    try:
        response = await client.responses.parse(
            model=settings.OPENAI_MODEL,
            input=[
                {
                    "role": "system",
                    "content": (
                        "당신은 교육용 문제 출제 전문가입니다. 제공된 파일의 실제 내용만 근거로 "
                        "서로 중복되지 않는 객관식 문제를 최대 5개 만드세요. 모든 문제는 정답이 하나뿐이어야 하며, "
                        "보기는 정확히 4개, 정답 해설은 학습자가 이해할 수 있도록 구체적으로 작성하세요."
                    ),
                },
                {
                    "role": "user",
                    "content": f"파일명: {file_name}\n파일 형식: {file_type}\n\n파일 내용:\n{code_content[:50000]}",
                },
            ],
            text_format=GeneratedQuestionSet,
        )
        generated = response.output_parsed
        if generated is None:
            return {"success": False, "count": 0, "questions": [], "message": "OpenAI가 문항 생성을 완료하지 못했습니다.", "usage": _response_usage(response)}

        created = []
        for data in generated.questions:
            options = [option.strip() for option in data.options]
            if any(not option for option in options):
                continue
            question = Question(
                subject_id=subject_id,
                professor_id=professor_id,
                question_type=QuestionType.CODE,
                title=data.title.strip(),
                content=data.content.strip(),
                difficulty=data.difficulty,
                correct_answer=str(data.correct_option),
                correct_option=data.correct_option + 1,
                explanation=data.explanation.strip(),
                options=json.dumps(options, ensure_ascii=False),
                source_file=file_name,
                tags=file_type,
                code_snippet=code_content[:10000],
            )
            db.add(question)
            created.append(question)

        if not created:
            db.rollback()
            return {"success": False, "count": 0, "questions": [], "message": "검증을 통과한 문항이 없습니다."}
        db.commit()
        for question in created:
            db.refresh(question)
        return {
            "success": True,
            "count": len(created),
            "questions": [serialize_question(question) for question in created],
            "message": f"{file_name}에서 {len(created)}개의 문제를 생성하고 저장했습니다.",
            "usage": _response_usage(response),
        }
    except Exception as error:
        db.rollback()
        return {"success": False, "count": 0, "questions": [], "message": f"OpenAI 문제 생성 실패: {error}"}


async def generate_single_question(
    prompt: str, subject_id: int, db: Session, professor_id: int | None = None
) -> dict:
    """Compatibility wrapper used by the manual question generation endpoint."""
    result = await generate_questions_from_code(
        prompt, "직접 입력", subject_id, "txt", db, professor_id
    )
    if result["success"] and result["questions"]:
        return {"success": True, "question_id": result["questions"][0]["id"], "message": "문제를 생성했습니다."}
    return {"success": False, "message": result["message"]}
