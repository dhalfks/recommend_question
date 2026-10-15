from datetime import datetime, timezone
from decimal import Decimal, ROUND_HALF_UP
from uuid import UUID, uuid4
from urllib.parse import quote

from fastapi import APIRouter, Depends, File, Form, HTTPException, Query, Response, UploadFile, status
from sqlalchemy import func
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from models import (
    PublicExam,
    PublicExamAttempt,
    PublicExamAttemptAnswer,
    PublicExamQuestion,
    PublicExamRound,
    PublicExamSourceDocument,
    PublicExamSubject,
    User,
    UserRole,
    get_db,
)
from schemas.public_exams import (
    PublicExamCreate,
    PublicExamAnswerSave,
    PublicExamAttemptAnswerProgress,
    PublicExamAttemptProgress,
    PublicExamAttemptResult,
    PublicExamAttemptResultItem,
    PublicExamQuestionAdminResponse,
    PublicExamQuestionCreate,
    PublicExamQuestionStudentResponse,
    PublicExamQuestionUpdate,
    PublicExamDocumentPublishResponse,
    PublicExamDocumentUploadResponse,
    PublicExamResponse,
    PublicExamRoundCreate,
    PublicExamRoundResponse,
    PublicExamRoundUpdate,
    PublicExamSubjectCreate,
    PublicExamSubjectResponse,
    PublicExamSubjectUpdate,
    PublicExamSourceDocumentDetail,
    PublicExamSourceDocumentResponse,
    PublicExamUpdate,
    PublicExamWrongAnswers,
)
from services.auth import get_current_user, require_roles
from services.public_exam_documents import (
    delete_pdf,
    document_sha256,
    extract_pdf_pages,
    load_pdf,
    parse_question_candidates,
    store_pdf,
)
from config import settings


router = APIRouter()
admin_only = require_roles(UserRole.ADMIN)
student_only = require_roles(UserRole.STUDENT)


def _not_found(resource: str):
    raise HTTPException(status_code=404, detail=f"{resource}을(를) 찾을 수 없습니다.")


def _commit(db: Session, instance):
    try:
        db.commit()
    except IntegrityError as exc:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="중복되거나 연결할 수 없는 콘텐츠 값입니다.",
        ) from exc
    db.refresh(instance)
    return instance


def _get_exam(db: Session, exam_id: int) -> PublicExam:
    exam = db.query(PublicExam).filter(PublicExam.id == exam_id).first()
    if not exam:
        _not_found("시험")
    return exam


def _get_round(db: Session, round_id: int) -> PublicExamRound:
    exam_round = db.query(PublicExamRound).filter(PublicExamRound.id == round_id).first()
    if not exam_round:
        _not_found("시험 회차")
    return exam_round


def _get_subject(db: Session, subject_id: int) -> PublicExamSubject:
    subject = db.query(PublicExamSubject).filter(PublicExamSubject.id == subject_id).first()
    if not subject:
        _not_found("시험 과목")
    return subject


def _get_question(db: Session, question_id: int) -> PublicExamQuestion:
    question = (
        db.query(PublicExamQuestion)
        .filter(PublicExamQuestion.id == question_id)
        .first()
    )
    if not question:
        _not_found("기출 문항")
    return question


def _get_document(db: Session, document_id: int) -> PublicExamSourceDocument:
    document = (
        db.query(PublicExamSourceDocument)
        .filter(PublicExamSourceDocument.id == document_id)
        .first()
    )
    if not document:
        _not_found("PDF 문서")
    return document


def _document_payload(db: Session, document: PublicExamSourceDocument, detail: bool = False) -> dict:
    questions = (
        db.query(PublicExamQuestion)
        .filter(PublicExamQuestion.source_document_id == document.id)
        .order_by(PublicExamQuestion.question_number, PublicExamQuestion.id)
        .all()
    )
    payload = {
        "id": document.id,
        "round_id": document.round_id,
        "original_file_name": document.original_file_name,
        "source_url": document.source_url,
        "source_organization": document.source_organization,
        "source_notes": document.source_notes,
        "sha256": document.sha256,
        "uploaded_by": document.uploaded_by,
        "uploaded_at": document.uploaded_at,
        "question_count": len(questions),
        "verified_count": sum(q.answer_verification_status == "VERIFIED" for q in questions),
        "published_count": sum(q.publication_status == "PUBLISHED" for q in questions),
    }
    if detail:
        payload["questions"] = questions
    return payload


def _validate_round_publishable(db: Session, round_id: int) -> None:
    subjects = db.query(PublicExamSubject).filter(PublicExamSubject.round_id == round_id).all()
    if not subjects:
        raise HTTPException(status_code=409, detail="과목이 없는 회차는 공개할 수 없습니다.")
    unavailable = []
    for subject in subjects:
        count = db.query(PublicExamQuestion).filter(
            PublicExamQuestion.subject_id == subject.id,
            PublicExamQuestion.publication_status == "PUBLISHED",
            PublicExamQuestion.answer_verification_status == "VERIFIED",
        ).count()
        if count == 0:
            unavailable.append(subject.name)
    if unavailable:
        raise HTTPException(
            status_code=409,
            detail=f"게시·검수 완료 문항이 없는 과목이 있습니다: {', '.join(unavailable)}",
        )


def _public_question_query(db: Session):
    return (
        db.query(PublicExamQuestion)
        .join(PublicExamSubject, PublicExamQuestion.subject_id == PublicExamSubject.id)
        .join(PublicExamRound, PublicExamSubject.round_id == PublicExamRound.id)
        .join(PublicExam, PublicExamRound.exam_id == PublicExam.id)
        .filter(
            PublicExam.is_active.is_(True),
            PublicExamRound.is_published.is_(True),
            PublicExamQuestion.publication_status == "PUBLISHED",
            PublicExamQuestion.answer_verification_status == "VERIFIED",
        )
    )


def _public_subject_query(db: Session):
    return (
        db.query(PublicExamSubject)
        .join(PublicExamRound, PublicExamSubject.round_id == PublicExamRound.id)
        .join(PublicExam, PublicExamRound.exam_id == PublicExam.id)
        .filter(
            PublicExam.is_active.is_(True),
            PublicExamRound.is_published.is_(True),
        )
    )


def _owned_attempt_query(
    db: Session,
    attempt_id: UUID,
    user_id: int,
) :
    return (
        db.query(PublicExamAttempt)
        .filter(
            PublicExamAttempt.id == attempt_id,
            PublicExamAttempt.user_id == user_id,
        )
    )


def _locked_owned_attempt(
    db: Session,
    attempt_id: UUID,
    user_id: int,
) -> PublicExamAttempt:
    attempt = _owned_attempt_query(db, attempt_id, user_id).with_for_update().first()
    if not attempt:
        _not_found("응시 기록")
    return attempt


def _owned_attempt(
    db: Session,
    attempt_id: UUID,
    user_id: int,
) -> PublicExamAttempt:
    attempt = _owned_attempt_query(db, attempt_id, user_id).first()
    if not attempt:
        _not_found("응시 기록")
    return attempt


def _require_in_progress(attempt: PublicExamAttempt):
    if attempt.status != "IN_PROGRESS":
        raise HTTPException(
            status_code=409,
            detail="진행 중인 응시만 변경하거나 제출할 수 있습니다.",
        )


def _normalized_text(value: str | None) -> str:
    return (value or "").strip().replace("\r\n", "\n")


def _grade_public_exam_answer(
    question: PublicExamQuestion,
    answer: PublicExamAttemptAnswer,
) -> bool:
    if question.answer_verification_status != "VERIFIED":
        raise HTTPException(
            status_code=409,
            detail="검수 상태가 변경된 문항이 있어 제출할 수 없습니다.",
        )
    if question.question_type == "MULTIPLE_CHOICE":
        if question.correct_option is None:
            raise HTTPException(status_code=409, detail="확인된 정답이 없는 문항입니다.")
        return answer.selected_option == question.correct_option
    if not _normalized_text(question.correct_answer):
        raise HTTPException(status_code=409, detail="확인된 정답이 없는 문항입니다.")
    return _normalized_text(answer.written_answer) == _normalized_text(
        question.correct_answer
    )


def _server_elapsed_seconds(started_at: datetime, submitted_at: datetime) -> int:
    return max(0, int((submitted_at - started_at).total_seconds()))


def _attempt_progress_payload(db: Session, attempt: PublicExamAttempt) -> dict:
    rows = (
        db.query(PublicExamAttemptAnswer, PublicExamQuestion)
        .join(
            PublicExamQuestion,
            PublicExamAttemptAnswer.question_id == PublicExamQuestion.id,
        )
        .filter(PublicExamAttemptAnswer.attempt_id == attempt.id)
        .order_by(PublicExamAttemptAnswer.sequence_number)
        .all()
    )
    return {
        "id": attempt.id,
        "subject_id": attempt.subject_id,
        "status": attempt.status,
        "started_at": attempt.started_at,
        "last_activity_at": attempt.last_activity_at,
        "total_questions": len(rows),
        "answers": [
            {
                "question": question,
                "sequence_number": answer.sequence_number,
                "selected_option": answer.selected_option,
                "written_answer": answer.written_answer,
                "elapsed_seconds": float(answer.elapsed_seconds or 0),
                "answered_at": answer.answered_at,
            }
            for answer, question in rows
        ],
    }


def _result_payload(db: Session, attempt: PublicExamAttempt) -> dict:
    if attempt.status != "SUBMITTED":
        raise HTTPException(status_code=409, detail="제출 완료된 응시가 아닙니다.")
    rows = (
        db.query(PublicExamAttemptAnswer, PublicExamQuestion)
        .join(
            PublicExamQuestion,
            PublicExamAttemptAnswer.question_id == PublicExamQuestion.id,
        )
        .filter(PublicExamAttemptAnswer.attempt_id == attempt.id)
        .order_by(PublicExamAttemptAnswer.sequence_number)
        .all()
    )
    subject = _get_subject(db, attempt.subject_id)
    exam_round = _get_round(db, subject.round_id)
    exam = _get_exam(db, exam_round.exam_id)
    items = [
        {
            "question_id": question.id,
            "sequence_number": answer.sequence_number,
            "question_number": question.question_number,
            "content": question.content,
            "options": question.options,
            "question_type": question.question_type,
            "selected_option": answer.selected_option,
            "written_answer": answer.written_answer,
            "correct_option": question.correct_option,
            "correct_answer": question.correct_answer,
            "explanation": question.explanation,
            "elapsed_seconds": float(answer.elapsed_seconds or 0),
            "is_correct": bool(answer.is_correct),
        }
        for answer, question in rows
    ]
    return {
        "attempt_id": attempt.id,
        "exam_name": exam.name,
        "exam_year": exam_round.exam_year,
        "round_identifier": exam_round.round_identifier,
        "subject_name": subject.name,
        "status": attempt.status,
        "started_at": attempt.started_at,
        "submitted_at": attempt.submitted_at,
        "total_elapsed_seconds": attempt.total_elapsed_seconds,
        "total_questions": attempt.total_questions,
        "correct_answers": attempt.correct_answers,
        "incorrect_answers": attempt.incorrect_answers,
        "score_percent": float(attempt.score_percent),
        "items": items,
    }


def _validate_source_document(
    db: Session,
    source_document_id: int | None,
    subject: PublicExamSubject,
):
    if source_document_id is None:
        return
    document = (
        db.query(PublicExamSourceDocument)
        .filter(PublicExamSourceDocument.id == source_document_id)
        .first()
    )
    if not document:
        _not_found("원본 문서")
    if document.round_id != subject.round_id:
        raise HTTPException(
            status_code=400,
            detail="원본 문서는 문항 과목과 같은 시험 회차에 속해야 합니다.",
        )


def _validated_question_update(
    question: PublicExamQuestion,
    payload: PublicExamQuestionUpdate,
) -> dict:
    current = {
        "source_document_id": question.source_document_id,
        "question_number": question.question_number,
        "content": question.content,
        "options": question.options,
        "question_type": question.question_type,
        "correct_option": question.correct_option,
        "correct_answer": question.correct_answer,
        "explanation": question.explanation,
        "source_page": question.source_page,
        "answer_verification_status": question.answer_verification_status,
        "publication_status": question.publication_status,
        "review_notes": question.review_notes,
    }
    changes = payload.model_dump(exclude_unset=True)
    PublicExamQuestionCreate(**{**current, **changes})
    return changes


# Public, authenticated content reads. Answers and explanations use a separate schema
# and are never serialized by these handlers.
@router.get("", response_model=list[PublicExamResponse])
async def list_public_exams(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return (
        db.query(PublicExam)
        .filter(PublicExam.is_active.is_(True))
        .order_by(PublicExam.name, PublicExam.id)
        .all()
    )


@router.get("/{exam_id}/rounds", response_model=list[PublicExamRoundResponse])
async def list_public_exam_rounds(
    exam_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    exam = _get_exam(db, exam_id)
    if not exam.is_active:
        _not_found("시험")
    return (
        db.query(PublicExamRound)
        .filter(
            PublicExamRound.exam_id == exam_id,
            PublicExamRound.is_published.is_(True),
        )
        .order_by(
            PublicExamRound.exam_year.desc(),
            PublicExamRound.round_identifier,
            PublicExamRound.id,
        )
        .all()
    )


@router.get("/rounds/{round_id}/subjects", response_model=list[PublicExamSubjectResponse])
async def list_public_exam_subjects(
    round_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    exam_round = (
        db.query(PublicExamRound)
        .join(PublicExam, PublicExamRound.exam_id == PublicExam.id)
        .filter(
            PublicExamRound.id == round_id,
            PublicExamRound.is_published.is_(True),
            PublicExam.is_active.is_(True),
        )
        .first()
    )
    if not exam_round:
        _not_found("공개 시험 회차")
    return (
        db.query(PublicExamSubject)
        .filter(PublicExamSubject.round_id == round_id)
        .order_by(PublicExamSubject.display_order, PublicExamSubject.id)
        .all()
    )


@router.get(
    "/subjects/{subject_id}/questions",
    response_model=list[PublicExamQuestionStudentResponse],
)
async def list_public_exam_questions(
    subject_id: int,
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=100, ge=1, le=200),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return (
        _public_question_query(db)
        .filter(PublicExamQuestion.subject_id == subject_id)
        .order_by(PublicExamQuestion.question_number, PublicExamQuestion.id)
        .offset(skip)
        .limit(limit)
        .all()
    )


@router.get(
    "/questions/{question_id}",
    response_model=PublicExamQuestionStudentResponse,
)
async def get_public_exam_question(
    question_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    question = (
        _public_question_query(db)
        .filter(PublicExamQuestion.id == question_id)
        .first()
    )
    if not question:
        _not_found("공개 기출 문항")
    return question


@router.post(
    "/subjects/{subject_id}/attempts",
    response_model=PublicExamAttemptProgress,
    status_code=201,
)
async def start_public_exam_attempt(
    subject_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(student_only),
):
    subject = (
        _public_subject_query(db)
        .filter(PublicExamSubject.id == subject_id)
        .first()
    )
    if not subject:
        _not_found("공개 시험 과목")

    # Serializes concurrent start requests for the same student. This closes the gap
    # left by the non-unique resume index without requiring another migration.
    db.query(User).filter(User.id == current_user.id).with_for_update().one()
    existing = (
        db.query(PublicExamAttempt)
        .filter(
            PublicExamAttempt.user_id == current_user.id,
            PublicExamAttempt.subject_id == subject_id,
            PublicExamAttempt.status == "IN_PROGRESS",
        )
        .order_by(PublicExamAttempt.started_at.desc())
        .with_for_update()
        .first()
    )
    if existing:
        return _attempt_progress_payload(db, existing)

    questions = (
        _public_question_query(db)
        .filter(PublicExamQuestion.subject_id == subject_id)
        .order_by(PublicExamQuestion.question_number, PublicExamQuestion.id)
        .all()
    )
    if not questions:
        raise HTTPException(
            status_code=409,
            detail="응시할 수 있는 검수 완료 공개 문항이 없습니다.",
        )

    attempt = PublicExamAttempt(
        id=uuid4(),
        user_id=current_user.id,
        subject_id=subject_id,
        status="IN_PROGRESS",
        total_questions=len(questions),
    )
    db.add(attempt)
    db.flush()
    db.add_all(
        [
            PublicExamAttemptAnswer(
                attempt_id=attempt.id,
                question_id=question.id,
                sequence_number=index,
                elapsed_seconds=Decimal("0"),
            )
            for index, question in enumerate(questions, start=1)
        ]
    )
    db.commit()
    db.refresh(attempt)
    return _attempt_progress_payload(db, attempt)


@router.get(
    "/attempts/in-progress",
    response_model=list[PublicExamAttemptProgress],
)
async def list_in_progress_public_exam_attempts(
    subject_id: int | None = Query(default=None),
    db: Session = Depends(get_db),
    current_user: User = Depends(student_only),
):
    query = db.query(PublicExamAttempt).filter(
        PublicExamAttempt.user_id == current_user.id,
        PublicExamAttempt.status == "IN_PROGRESS",
    )
    if subject_id is not None:
        query = query.filter(PublicExamAttempt.subject_id == subject_id)
    attempts = query.order_by(PublicExamAttempt.last_activity_at.desc()).all()
    return [_attempt_progress_payload(db, attempt) for attempt in attempts]


@router.get(
    "/attempts/{attempt_id}",
    response_model=PublicExamAttemptProgress,
)
async def get_public_exam_attempt(
    attempt_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(student_only),
):
    attempt = _owned_attempt(db, attempt_id, current_user.id)
    _require_in_progress(attempt)
    return _attempt_progress_payload(db, attempt)


@router.put(
    "/attempts/{attempt_id}/answers/{question_id}",
    response_model=PublicExamAttemptAnswerProgress,
)
async def save_public_exam_answer(
    attempt_id: UUID,
    question_id: int,
    payload: PublicExamAnswerSave,
    db: Session = Depends(get_db),
    current_user: User = Depends(student_only),
):
    attempt = _locked_owned_attempt(db, attempt_id, current_user.id)
    _require_in_progress(attempt)
    row = (
        db.query(PublicExamAttemptAnswer, PublicExamQuestion)
        .join(
            PublicExamQuestion,
            PublicExamAttemptAnswer.question_id == PublicExamQuestion.id,
        )
        .filter(
            PublicExamAttemptAnswer.attempt_id == attempt.id,
            PublicExamAttemptAnswer.question_id == question_id,
        )
        .first()
    )
    if not row:
        _not_found("응시 문항")
    answer, question = row

    if question.question_type == "MULTIPLE_CHOICE":
        if payload.written_answer is not None:
            raise HTTPException(status_code=400, detail="객관식 문항에는 보기 번호를 저장해야 합니다.")
        if payload.selected_option is not None and (
            not question.options or payload.selected_option > len(question.options)
        ):
            raise HTTPException(status_code=400, detail="유효하지 않은 보기 번호입니다.")
    elif payload.selected_option is not None:
        raise HTTPException(status_code=400, detail="단답형 문항에는 텍스트 답안을 저장해야 합니다.")

    now = db.query(func.clock_timestamp()).scalar()
    answer.selected_option = payload.selected_option
    answer.written_answer = payload.written_answer
    answer.elapsed_seconds = Decimal(str(payload.elapsed_seconds))
    answer.answered_at = (
        now
        if payload.selected_option is not None or _normalized_text(payload.written_answer)
        else None
    )
    answer.updated_at = now
    attempt.last_activity_at = now
    attempt.updated_at = now
    db.commit()
    return {
        "question": question,
        "sequence_number": answer.sequence_number,
        "selected_option": answer.selected_option,
        "written_answer": answer.written_answer,
        "elapsed_seconds": float(answer.elapsed_seconds),
        "answered_at": answer.answered_at,
    }


@router.post(
    "/attempts/{attempt_id}/submit",
    response_model=PublicExamAttemptResult,
)
async def submit_public_exam_attempt(
    attempt_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(student_only),
):
    attempt = _locked_owned_attempt(db, attempt_id, current_user.id)
    _require_in_progress(attempt)
    rows = (
        db.query(PublicExamAttemptAnswer, PublicExamQuestion)
        .join(
            PublicExamQuestion,
            PublicExamAttemptAnswer.question_id == PublicExamQuestion.id,
        )
        .filter(PublicExamAttemptAnswer.attempt_id == attempt.id)
        .order_by(PublicExamAttemptAnswer.sequence_number)
        .with_for_update(of=PublicExamAttemptAnswer)
        .all()
    )
    if not rows:
        raise HTTPException(status_code=409, detail="응시 문항이 없어 제출할 수 없습니다.")

    submitted_at = db.query(func.clock_timestamp()).scalar()
    correct_count = 0
    for answer, question in rows:
        answer.is_correct = _grade_public_exam_answer(question, answer)
        answer.graded_at = submitted_at
        answer.updated_at = submitted_at
        if answer.is_correct:
            correct_count += 1

    total_count = len(rows)
    incorrect_count = total_count - correct_count
    score_percent = (
        (Decimal(correct_count) * Decimal("100") / Decimal(total_count)).quantize(
            Decimal("0.01"), rounding=ROUND_HALF_UP
        )
    )
    attempt.status = "SUBMITTED"
    attempt.submitted_at = submitted_at
    attempt.total_elapsed_seconds = _server_elapsed_seconds(
        attempt.started_at, submitted_at
    )
    attempt.total_questions = total_count
    attempt.correct_answers = correct_count
    attempt.incorrect_answers = incorrect_count
    attempt.score_percent = score_percent
    attempt.last_activity_at = submitted_at
    attempt.updated_at = submitted_at
    db.commit()
    db.refresh(attempt)
    return _result_payload(db, attempt)


@router.get(
    "/attempts/{attempt_id}/result",
    response_model=PublicExamAttemptResult,
)
async def get_public_exam_attempt_result(
    attempt_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(student_only),
):
    attempt = _owned_attempt(db, attempt_id, current_user.id)
    return _result_payload(db, attempt)


@router.get(
    "/attempts/{attempt_id}/wrong-answers",
    response_model=PublicExamWrongAnswers,
)
async def get_public_exam_wrong_answers(
    attempt_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(student_only),
):
    attempt = _owned_attempt(db, attempt_id, current_user.id)
    result = _result_payload(db, attempt)
    return {
        "attempt_id": attempt.id,
        "items": [item for item in result["items"] if not item["is_correct"]],
    }


# Admin content management.
@router.get(
    "/admin/documents",
    response_model=list[PublicExamSourceDocumentResponse],
)
async def list_public_exam_documents_for_admin(
    round_id: int | None = Query(default=None),
    db: Session = Depends(get_db),
    current_user: User = Depends(admin_only),
):
    query = db.query(PublicExamSourceDocument)
    if round_id is not None:
        query = query.filter(PublicExamSourceDocument.round_id == round_id)
    documents = query.order_by(PublicExamSourceDocument.uploaded_at.desc()).all()
    return [_document_payload(db, document) for document in documents]


@router.get(
    "/admin/documents/{document_id}",
    response_model=PublicExamSourceDocumentDetail,
)
async def get_public_exam_document_for_admin(
    document_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(admin_only),
):
    return _document_payload(db, _get_document(db, document_id), detail=True)


@router.get("/admin/documents/{document_id}/file")
async def download_public_exam_document_for_admin(
    document_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(admin_only),
):
    document = _get_document(db, document_id)
    if not document.storage_key:
        _not_found("저장된 PDF")
    try:
        content = await load_pdf(document.storage_key)
    except FileNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    encoded_name = quote(document.original_file_name)
    return Response(
        content=content,
        media_type="application/pdf",
        headers={"Content-Disposition": f"inline; filename*=UTF-8''{encoded_name}"},
    )


@router.post(
    "/admin/subjects/{subject_id}/documents",
    response_model=PublicExamDocumentUploadResponse,
    status_code=201,
)
async def upload_public_exam_document_for_admin(
    subject_id: int,
    file: UploadFile = File(...),
    source_url: str | None = Form(default=None),
    source_organization: str | None = Form(default=None),
    source_notes: str | None = Form(default=None),
    is_test_data: bool = Form(default=False),
    db: Session = Depends(get_db),
    current_user: User = Depends(admin_only),
):
    subject = _get_subject(db, subject_id)
    filename = file.filename or "document.pdf"
    if not filename.lower().endswith(".pdf") or file.content_type not in {
        "application/pdf", "application/octet-stream"
    }:
        raise HTTPException(status_code=400, detail="PDF 파일만 등록할 수 있습니다.")
    data = await file.read(settings.PUBLIC_EXAM_PDF_MAX_BYTES + 1)
    await file.close()
    if not data:
        raise HTTPException(status_code=400, detail="빈 PDF 파일은 등록할 수 없습니다.")
    if len(data) > settings.PUBLIC_EXAM_PDF_MAX_BYTES:
        raise HTTPException(
            status_code=413,
            detail=f"PDF 파일은 {settings.PUBLIC_EXAM_PDF_MAX_BYTES // (1024 * 1024)}MB 이하여야 합니다.",
        )
    if not data.startswith(b"%PDF-"):
        raise HTTPException(status_code=400, detail="올바른 PDF 파일이 아닙니다.")

    digest = document_sha256(data)
    duplicate = db.query(PublicExamSourceDocument).filter(
        PublicExamSourceDocument.round_id == subject.round_id,
        PublicExamSourceDocument.sha256 == digest,
    ).first()
    if duplicate:
        raise HTTPException(status_code=409, detail="이 회차에 동일한 PDF가 이미 등록되어 있습니다.")
    try:
        candidates = parse_question_candidates(extract_pdf_pages(data))
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc
    if not candidates:
        raise HTTPException(
            status_code=422,
            detail="문항 번호를 인식하지 못했습니다. 텍스트 PDF인지 확인해 주세요.",
        )

    existing_numbers = {
        row[0] for row in db.query(PublicExamQuestion.question_number)
        .filter(PublicExamQuestion.subject_id == subject_id).all()
    }
    collisions = sorted({item.question_number for item in candidates} & existing_numbers)
    if collisions:
        raise HTTPException(
            status_code=409,
            detail=f"이미 등록된 문항 번호가 있습니다: {', '.join(map(str, collisions))}",
        )

    storage_key = await store_pdf(data, filename)
    notes = (source_notes or "").strip() or None
    if is_test_data:
        notes = f"[TEST DATA] {notes or '관리자 테스트용 문서'}"
    document = PublicExamSourceDocument(
        round_id=subject.round_id,
        original_file_name=filename,
        storage_key=storage_key,
        source_url=(source_url or "").strip() or None,
        source_organization=(source_organization or "").strip() or None,
        source_notes=notes,
        sha256=digest,
        uploaded_by=current_user.id,
    )
    try:
        db.add(document)
        db.flush()
        db.add_all([
            PublicExamQuestion(
                subject_id=subject_id,
                source_document_id=document.id,
                question_number=item.question_number,
                content=item.content,
                options=item.options,
                question_type="MULTIPLE_CHOICE" if item.options else "SHORT_ANSWER",
                source_page=item.source_page,
                answer_verification_status="MISSING",
                publication_status="DRAFT",
                review_notes="PDF 자동 추출 후보: 원문과 대조 후 정답 및 내용을 검수하세요.",
            )
            for item in candidates
        ])
        db.commit()
        db.refresh(document)
    except Exception:
        db.rollback()
        await delete_pdf(storage_key)
        raise
    payload = _document_payload(db, document, detail=True)
    payload["extraction_message"] = (
        f"{len(candidates)}개 문항 후보를 DRAFT로 등록했습니다. 정답은 자동 추측하지 않았습니다."
    )
    return payload


@router.post(
    "/admin/documents/{document_id}/publish",
    response_model=PublicExamDocumentPublishResponse,
)
async def publish_public_exam_document_for_admin(
    document_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(admin_only),
):
    document = _get_document(db, document_id)
    questions = (
        db.query(PublicExamQuestion)
        .filter(PublicExamQuestion.source_document_id == document.id)
        .with_for_update()
        .all()
    )
    if not questions:
        raise HTTPException(status_code=409, detail="게시할 문항이 없습니다.")
    invalid = [
        question.question_number for question in questions
        if question.answer_verification_status != "VERIFIED"
        or (question.question_type == "MULTIPLE_CHOICE" and question.correct_option is None)
        or (question.question_type == "SHORT_ANSWER" and not _normalized_text(question.correct_answer))
    ]
    if invalid:
        raise HTTPException(
            status_code=409,
            detail=f"정답 검수가 완료되지 않은 문항이 있습니다: {', '.join(map(str, sorted(invalid)))}",
        )
    for question in questions:
        question.publication_status = "PUBLISHED"
        question.updated_at = datetime.now(timezone.utc)
    db.commit()
    return {"document_id": document.id, "published_count": len(questions)}


@router.get("/admin/exams", response_model=list[PublicExamResponse])
async def list_public_exams_for_admin(
    db: Session = Depends(get_db),
    current_user: User = Depends(admin_only),
):
    return db.query(PublicExam).order_by(PublicExam.name, PublicExam.id).all()


@router.get(
    "/admin/exams/{exam_id}/rounds",
    response_model=list[PublicExamRoundResponse],
)
async def list_public_exam_rounds_for_admin(
    exam_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(admin_only),
):
    _get_exam(db, exam_id)
    return (
        db.query(PublicExamRound)
        .filter(PublicExamRound.exam_id == exam_id)
        .order_by(
            PublicExamRound.exam_year.desc(),
            PublicExamRound.round_identifier,
            PublicExamRound.id,
        )
        .all()
    )


@router.get(
    "/admin/rounds/{round_id}/subjects",
    response_model=list[PublicExamSubjectResponse],
)
async def list_public_exam_subjects_for_admin(
    round_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(admin_only),
):
    _get_round(db, round_id)
    return (
        db.query(PublicExamSubject)
        .filter(PublicExamSubject.round_id == round_id)
        .order_by(PublicExamSubject.display_order, PublicExamSubject.id)
        .all()
    )


@router.get(
    "/admin/subjects/{subject_id}/questions",
    response_model=list[PublicExamQuestionAdminResponse],
)
async def list_public_exam_questions_for_admin(
    subject_id: int,
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=100, ge=1, le=200),
    db: Session = Depends(get_db),
    current_user: User = Depends(admin_only),
):
    _get_subject(db, subject_id)
    return (
        db.query(PublicExamQuestion)
        .filter(PublicExamQuestion.subject_id == subject_id)
        .order_by(PublicExamQuestion.question_number, PublicExamQuestion.id)
        .offset(skip)
        .limit(limit)
        .all()
    )


@router.post("", response_model=PublicExamResponse, status_code=201)
async def create_public_exam(
    payload: PublicExamCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(admin_only),
):
    exam = PublicExam(**payload.model_dump())
    db.add(exam)
    return _commit(db, exam)


@router.put("/{exam_id}", response_model=PublicExamResponse)
async def update_public_exam(
    exam_id: int,
    payload: PublicExamUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(admin_only),
):
    exam = _get_exam(db, exam_id)
    for key, value in payload.model_dump(exclude_unset=True).items():
        setattr(exam, key, value)
    exam.updated_at = datetime.now(timezone.utc)
    return _commit(db, exam)


@router.post("/{exam_id}/rounds", response_model=PublicExamRoundResponse, status_code=201)
async def create_public_exam_round(
    exam_id: int,
    payload: PublicExamRoundCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(admin_only),
):
    _get_exam(db, exam_id)
    exam_round = PublicExamRound(exam_id=exam_id, **payload.model_dump())
    db.add(exam_round)
    return _commit(db, exam_round)


@router.put("/rounds/{round_id}", response_model=PublicExamRoundResponse)
async def update_public_exam_round(
    round_id: int,
    payload: PublicExamRoundUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(admin_only),
):
    exam_round = _get_round(db, round_id)
    changes = payload.model_dump(exclude_unset=True)
    if changes.get("is_published") is True:
        _validate_round_publishable(db, round_id)
    for key, value in changes.items():
        setattr(exam_round, key, value)
    exam_round.updated_at = datetime.now(timezone.utc)
    return _commit(db, exam_round)


@router.post(
    "/rounds/{round_id}/subjects",
    response_model=PublicExamSubjectResponse,
    status_code=201,
)
async def create_public_exam_subject(
    round_id: int,
    payload: PublicExamSubjectCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(admin_only),
):
    _get_round(db, round_id)
    subject = PublicExamSubject(round_id=round_id, **payload.model_dump())
    db.add(subject)
    return _commit(db, subject)


@router.put("/subjects/{subject_id}", response_model=PublicExamSubjectResponse)
async def update_public_exam_subject(
    subject_id: int,
    payload: PublicExamSubjectUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(admin_only),
):
    subject = _get_subject(db, subject_id)
    for key, value in payload.model_dump(exclude_unset=True).items():
        setattr(subject, key, value)
    subject.updated_at = datetime.now(timezone.utc)
    return _commit(db, subject)


@router.post(
    "/subjects/{subject_id}/questions",
    response_model=PublicExamQuestionAdminResponse,
    status_code=201,
)
async def create_public_exam_question(
    subject_id: int,
    payload: PublicExamQuestionCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(admin_only),
):
    subject = _get_subject(db, subject_id)
    _validate_source_document(db, payload.source_document_id, subject)
    question = PublicExamQuestion(subject_id=subject_id, **payload.model_dump())
    db.add(question)
    return _commit(db, question)


@router.get(
    "/admin/questions/{question_id}",
    response_model=PublicExamQuestionAdminResponse,
)
async def get_public_exam_question_for_admin(
    question_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(admin_only),
):
    return _get_question(db, question_id)


@router.put(
    "/questions/{question_id}",
    response_model=PublicExamQuestionAdminResponse,
)
async def update_public_exam_question(
    question_id: int,
    payload: PublicExamQuestionUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(admin_only),
):
    question = _get_question(db, question_id)
    changes = _validated_question_update(question, payload)
    subject = _get_subject(db, question.subject_id)
    _validate_source_document(
        db, changes.get("source_document_id", question.source_document_id), subject
    )
    for key, value in changes.items():
        setattr(question, key, value)
    question.updated_at = datetime.now(timezone.utc)
    return _commit(db, question)
