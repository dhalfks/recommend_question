import json

from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy import func
from sqlalchemy.orm import Session, selectinload

from models import ExamPaper, ExamPaperItem, Question, Subject, User, UserRole, get_db
from schemas.exam_papers import ExamPaperResponse, ExamPaperSummaryResponse, ExamPaperWrite
from services.auth import require_roles


router = APIRouter()
professor_only = require_roles(UserRole.PROFESSOR)


def _owned_paper_query(db: Session, professor_id: int):
    return db.query(ExamPaper).filter(ExamPaper.professor_id == professor_id)


def _owned_paper(db: Session, paper_id: int, professor_id: int) -> ExamPaper:
    paper = (
        _owned_paper_query(db, professor_id)
        .options(selectinload(ExamPaper.items))
        .filter(ExamPaper.id == paper_id)
        .first()
    )
    if paper is None:
        raise HTTPException(status_code=404, detail="시험지를 찾을 수 없습니다.")
    return paper


def _parse_options(raw: str | None) -> list[str] | None:
    if not raw:
        return None
    try:
        parsed = json.loads(raw)
    except (TypeError, json.JSONDecodeError):
        return None
    if not isinstance(parsed, list):
        return None
    return [str(option) for option in parsed]


def _paper_items(
    db: Session, professor_id: int, question_ids: list[int]
) -> list[ExamPaperItem]:
    rows = (
        db.query(Question, Subject.name)
        .join(Subject, Subject.id == Question.subject_id)
        .filter(
            Question.id.in_(question_ids),
            Question.professor_id == professor_id,
        )
        .all()
    )
    by_id = {question.id: (question, subject_name) for question, subject_name in rows}
    missing = [question_id for question_id in question_ids if question_id not in by_id]
    if missing:
        raise HTTPException(
            status_code=400,
            detail="본인이 소유하지 않거나 존재하지 않는 문항이 포함되어 있습니다.",
        )

    items: list[ExamPaperItem] = []
    for order, question_id in enumerate(question_ids, start=1):
        question, subject_name = by_id[question_id]
        answer_type = (
            question.answer_type.value
            if hasattr(question.answer_type, "value")
            else str(question.answer_type)
        )
        items.append(ExamPaperItem(
            question_id=question.id,
            display_order=order,
            subject_id=question.subject_id,
            subject_name=subject_name,
            title=question.title,
            content=question.content,
            answer_type=answer_type,
            options=_parse_options(question.options),
            code_snippet=question.code_snippet,
            correct_answer=question.correct_answer,
            correct_option=question.correct_option,
            explanation=question.explanation,
        ))
    return items


def _summary(paper: ExamPaper) -> dict:
    return {
        "id": paper.id,
        "title": paper.title,
        "description": paper.description,
        "item_count": len(paper.items),
        "created_at": paper.created_at,
        "updated_at": paper.updated_at,
    }


@router.get("", response_model=list[ExamPaperSummaryResponse])
async def list_exam_papers(
    db: Session = Depends(get_db),
    current_user: User = Depends(professor_only),
):
    papers = (
        _owned_paper_query(db, current_user.id)
        .options(selectinload(ExamPaper.items))
        .order_by(ExamPaper.updated_at.desc(), ExamPaper.id.desc())
        .all()
    )
    return [_summary(paper) for paper in papers]


@router.post("", response_model=ExamPaperResponse, status_code=status.HTTP_201_CREATED)
async def create_exam_paper(
    payload: ExamPaperWrite,
    db: Session = Depends(get_db),
    current_user: User = Depends(professor_only),
):
    paper = ExamPaper(
        professor_id=current_user.id,
        title=payload.title,
        description=payload.description.strip() if payload.description else None,
    )
    paper.items = _paper_items(db, current_user.id, payload.question_ids)
    db.add(paper)
    db.commit()
    return _owned_paper(db, paper.id, current_user.id)


@router.get("/{paper_id}", response_model=ExamPaperResponse)
async def get_exam_paper(
    paper_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(professor_only),
):
    return _owned_paper(db, paper_id, current_user.id)


@router.put("/{paper_id}", response_model=ExamPaperResponse)
async def update_exam_paper(
    paper_id: int,
    payload: ExamPaperWrite,
    db: Session = Depends(get_db),
    current_user: User = Depends(professor_only),
):
    paper = _owned_paper(db, paper_id, current_user.id)
    replacement_items = _paper_items(db, current_user.id, payload.question_ids)
    paper.title = payload.title
    paper.description = payload.description.strip() if payload.description else None
    paper.items.clear()
    db.flush()
    paper.items.extend(replacement_items)
    paper.updated_at = func.now()
    db.commit()
    return _owned_paper(db, paper.id, current_user.id)


@router.delete("/{paper_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_exam_paper(
    paper_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(professor_only),
):
    paper = _owned_paper(db, paper_id, current_user.id)
    db.delete(paper)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
