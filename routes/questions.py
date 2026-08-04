from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import func
import random

from models import get_db, Question, Subject, User, UserRole
from services.auth import get_current_user, require_roles
from schemas.questions import (
    QuestionCreate, QuestionResponse, RandomQuestionsRequest, 
    RandomQuestionsResponse, QuestionUpdate
)

router = APIRouter()

# 모든 문제 조회
@router.get("/", response_model=list[QuestionResponse])
async def get_questions(
    subject_id: int = Query(None),
    difficulty: str = Query(None),
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=1000),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    query = db.query(Question)
    
    if subject_id:
        query = query.filter(Question.subject_id == subject_id)
    if difficulty:
        query = query.filter(Question.difficulty == difficulty)
    
    questions = query.offset(skip).limit(limit).all()
    return questions

@router.post("/admin/backfill-answers")
async def backfill_answers(
    limit: int = Query(100, ge=1, le=500),
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles(UserRole.ADMIN)),
):
    from services.answer_enrichment import backfill_missing_answers

    return await backfill_missing_answers(db, limit)

# 특정 문제 조회
@router.get("/subject-units")
async def get_subject_units(
    subject_id: int = Query(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    units = (
        db.query(Question.subject_unit)
        .filter(
            Question.subject_id == subject_id,
            Question.subject_unit.isnot(None),
            Question.subject_unit != "",
        )
        .distinct()
        .order_by(Question.subject_unit)
        .all()
    )
    return {"subject_units": [unit for (unit,) in units]}


@router.get("/{question_id}", response_model=QuestionResponse)
async def get_question(
    question_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    question = db.query(Question).filter(Question.id == question_id).first()
    if not question:
        raise HTTPException(status_code=404, detail="Question not found")
    return question

# 문제 생성
@router.post("/", response_model=QuestionResponse)
async def create_question(
    question: QuestionCreate,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_roles(UserRole.PROFESSOR, UserRole.ADMIN)
    ),
):
    # 과목 존재 확인
    subject = db.query(Subject).filter(Subject.id == question.subject_id).first()
    if not subject:
        raise HTTPException(status_code=404, detail="Subject not found")
    
    db_question = Question(
        subject_id=question.subject_id,
        question_type="EXCEL",
        title=question.title,
        content=question.content,
        correct_answer=question.correct_answer,
        explanation=question.explanation,
        difficulty=question.difficulty,
        source_file=question.source_file,
        options=question.options,
        tags=question.tags,
        code_snippet=question.code_snippet,
        answer_code_snippet=question.answer_code_snippet,
        is_required=question.is_required,
    )
    db.add(db_question)
    db.commit()
    db.refresh(db_question)
    from services.answer_enrichment import enrich_question_by_id

    background_tasks.add_task(enrich_question_by_id, db_question.id)
    return db_question


# 문제 수정
@router.put("/{question_id}", response_model=QuestionResponse)
async def update_question(
    question_id: int,
    question_update: QuestionUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_roles(UserRole.PROFESSOR, UserRole.ADMIN)
    ),
):
    db_question = db.query(Question).filter(Question.id == question_id).first()
    if not db_question:
        raise HTTPException(status_code=404, detail="Question not found")
    
    update_data = question_update.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_question, key, value)
    
    db.commit()
    db.refresh(db_question)
    return db_question

# 문제 삭제
@router.delete("/{question_id}")
async def delete_question(
    question_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_roles(UserRole.PROFESSOR, UserRole.ADMIN)
    ),
):
    db_question = db.query(Question).filter(Question.id == question_id).first()
    if not db_question:
        raise HTTPException(status_code=404, detail="Question not found")
    
    db.delete(db_question)
    db.commit()
    return {"message": "Question deleted successfully"}

# 랜덤 문제 출제
@router.post("/random/quiz", response_model=RandomQuestionsResponse)
async def get_random_questions(
    request: RandomQuestionsRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    query = db.query(Question)
    
    if request.subject_id:
        query = query.filter(Question.subject_id == request.subject_id)
    if request.subject_unit:
        query = query.filter(Question.subject_unit == request.subject_unit)
    if request.difficulty:
        query = query.filter(Question.difficulty == request.difficulty)
    
    total_count = query.count()
    
    if total_count == 0:
        raise HTTPException(status_code=404, detail="No questions found matching criteria")
    
    # 랜덤 선택
    questions = query.all()
    required_questions = [question for question in questions if question.is_required]
    regular_questions = [question for question in questions if not question.is_required]
    target_count = min(request.count, len(questions))
    selected_questions = random.sample(
        required_questions, min(target_count, len(required_questions))
    )
    remaining = target_count - len(selected_questions)
    if remaining:
        selected_questions.extend(random.sample(regular_questions, remaining))
    random.shuffle(selected_questions)
    
    return {
        "questions": selected_questions,
        "total_count": total_count
    }

# 난이도별 통계
@router.get("/stats/difficulty")
async def get_difficulty_stats(
    subject_id: int = Query(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    query = db.query(
        Question.difficulty,
        func.count(Question.id).label("count")
    )
    
    if subject_id:
        query = query.filter(Question.subject_id == subject_id)
    
    stats = query.group_by(Question.difficulty).all()
    return {
        "difficulty_stats": [
            {"difficulty": stat[0], "count": stat[1]} for stat in stats
        ]
    }
