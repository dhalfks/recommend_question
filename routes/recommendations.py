from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from models import User, UserRole, get_db
from services.auth import require_roles
from services.recommendation import (
    get_my_latest_wrong_questions,
    get_similar_learners_most_missed,
    get_similar_learners_most_missed_units,
    recommend_questions,
)

router = APIRouter()


@router.get("/peer-missed")
async def similar_learners_most_missed(
    count: int = Query(5, ge=1, le=20),
    subject_id: int | None = Query(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles(UserRole.STUDENT)),
):
    items = get_similar_learners_most_missed(
        db, current_user.id, count=count, subject_id=subject_id
    )
    return {"items": items, "total_count": len(items)}


@router.get("/quiz")
async def adaptive_quiz(
    count: int = Query(5, ge=1, le=20),
    subject_id: int | None = Query(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles(UserRole.STUDENT)),
):
    questions, metadata = recommend_questions(db, current_user.id, count, subject_id)
    if not questions:
        raise HTTPException(status_code=404, detail="추천할 문항이 없습니다.")
    return {
        "questions": questions,
        "total_count": len(questions),
        "recommendations": metadata,
        "algorithm": "hybrid_user_cf_item_similarity_adaptive",
    }


@router.get("/peer-missed-units")
async def similar_learners_most_missed_units(
    count: int = Query(5, ge=1, le=20),
    subject_id: int | None = Query(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles(UserRole.STUDENT)),
):
    items = get_similar_learners_most_missed_units(
        db, current_user.id, count=count, subject_id=subject_id
    )
    return {"items": items, "total_count": len(items)}


@router.get("/my-wrong")
async def my_latest_wrong_questions(
    count: int = Query(5, ge=1, le=20),
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles(UserRole.STUDENT)),
):
    items = get_my_latest_wrong_questions(db, current_user.id, count=count)
    return {"items": items, "total_count": len(items)}
