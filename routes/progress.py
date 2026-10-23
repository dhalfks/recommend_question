from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import String, case, func, or_
from sqlalchemy.orm import Session
from uuid import uuid4
import json

from models import (
    AnswerType,
    DifficultyLevel,
    Question,
    QuizSession,
    SessionLocal,
    Subject,
    User,
    UserProgress,
    UserRole,
    get_db,
)
from schemas.progress import QuizSubmission, QuizSubmissionResult
from services.auth import require_roles
from services.permissions import ensure_question_access, scope_questions

router = APIRouter()


def question_label(question: Question):
    return question.external_id or question.id


def option_payload(question: Question):
    try:
        values = json.loads(question.options or "[]")
        return values if isinstance(values, list) else []
    except (TypeError, ValueError):
        return []


@router.get("/question-analytics")
async def get_question_analytics(
    subject_id: int | None = Query(None),
    difficulty: str | None = Query(None),
    search: str | None = Query(None),
    min_wrong_rate: int = Query(0, ge=0, le=100),
    sort: str = Query("wrong_rate_desc"),
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=5, le=100),
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles(UserRole.PROFESSOR, UserRole.ADMIN)),
):
    """Return compact, server-side question aggregates for the teacher dashboard."""
    correct_count = func.sum(case((UserProgress.is_correct == "CORRECT", 1), else_=0))
    wrong_count = func.sum(case((UserProgress.is_correct == "INCORRECT", 1), else_=0))
    skipped_count = func.sum(case((UserProgress.is_correct == "SKIP", 1), else_=0))
    query = (
        db.query(
            Question,
            Subject.name.label("subject_name"),
            func.count(UserProgress.id).label("responses"),
            correct_count.label("correct"),
            wrong_count.label("wrong"),
            skipped_count.label("skipped"),
            func.avg(UserProgress.elapsed_seconds).label("average_seconds"),
        )
        .join(Subject, Question.subject_id == Subject.id)
        .outerjoin(UserProgress, UserProgress.question_id == Question.id)
    )
    if current_user.role == UserRole.PROFESSOR:
        query = query.filter(Question.professor_id == current_user.id)
    if subject_id:
        query = query.filter(Question.subject_id == subject_id)
    if difficulty:
        query = query.filter(Question.difficulty == difficulty)
    if search:
        term = f"%{search.strip()}%"
        query = query.filter(or_(Question.title.ilike(term), Question.content.ilike(term)))
    rows = query.group_by(Question.id, Subject.name).all()

    question_ids = [row.Question.id for row in rows]
    wrong_choices = {}
    if question_ids:
        choice_rows = (
            db.query(
                UserProgress.question_id,
                UserProgress.user_answer,
                func.count(UserProgress.id).label("count"),
            )
            .filter(
                UserProgress.question_id.in_(question_ids),
                UserProgress.is_correct == "INCORRECT",
                UserProgress.user_answer.isnot(None),
            )
            .group_by(UserProgress.question_id, UserProgress.user_answer)
            .all()
        )
        for choice in choice_rows:
            previous = wrong_choices.get(choice.question_id)
            if previous is None or choice.count > previous[1]:
                wrong_choices[choice.question_id] = (choice.user_answer, choice.count)

    items = []
    for row in rows:
        question = row.Question
        responses = int(row.responses or 0)
        correct = int(row.correct or 0)
        wrong = int(row.wrong or 0)
        skipped = int(row.skipped or 0)
        wrong_rate = round((wrong + skipped) / responses * 100, 1) if responses else 0
        popular = wrong_choices.get(question.id)
        popular_payload = None
        if popular:
            answer, count = popular
            options = option_payload(question)
            try:
                index = int(answer)
                label = str(options[index]) if 0 <= index < len(options) else answer
                display = f"{index + 1}번 · {label}"
            except (TypeError, ValueError):
                display = str(answer)
            popular_payload = {"answer": display, "count": int(count)}
        items.append({
            "question_id": question.id,
            "question_number": question_label(question),
            "title": question.title,
            "content": question.content,
            "subject_id": question.subject_id,
            "subject_name": row.subject_name,
            "difficulty": question.difficulty.value if hasattr(question.difficulty, "value") else str(question.difficulty),
            "responses": responses,
            "correct": correct,
            "wrong": wrong,
            "skipped": skipped,
            "correct_rate": round(correct / responses * 100, 1) if responses else 0,
            "wrong_rate": wrong_rate,
            "average_seconds": round(float(row.average_seconds or 0), 1),
            "most_common_wrong": popular_payload,
        })

    items = [item for item in items if item["wrong_rate"] >= min_wrong_rate]
    sorters = {
        "wrong_rate_desc": lambda item: (-item["wrong_rate"], item["question_number"]),
        "time_desc": lambda item: (-item["average_seconds"], item["question_number"]),
        "responses_desc": lambda item: (-item["responses"], item["question_number"]),
        "number_asc": lambda item: item["question_number"],
    }
    items.sort(key=sorters.get(sort, sorters["wrong_rate_desc"]))
    total = len(items)
    responded = [item for item in items if item["responses"]]
    total_responses = sum(item["responses"] for item in responded)
    total_correct = sum(item["correct"] for item in responded)
    start = (page - 1) * page_size
    return {
        "summary": {
            "questions": total,
            "responses": total_responses,
            "correct_rate": round(total_correct / total_responses * 100, 1) if total_responses else 0,
            "average_seconds": round(sum(item["average_seconds"] * item["responses"] for item in responded) / total_responses, 1) if total_responses else 0,
            "highest_wrong": max(responded, key=lambda item: item["wrong_rate"], default=None),
            "slowest": max(responded, key=lambda item: item["average_seconds"], default=None),
        },
        "items": items[start:start + page_size],
        "total": total,
        "page": page,
        "page_size": page_size,
    }


@router.get("/question-analytics/{question_id}")
async def get_question_analytics_detail(
    question_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles(UserRole.PROFESSOR, UserRole.ADMIN)),
):
    question = ensure_question_access(
        db.query(Question).filter(Question.id == question_id).first(), current_user
    )
    attempts = (
        db.query(UserProgress, User)
        .outerjoin(User, func.cast(User.id, String) == UserProgress.user_id)
        .filter(UserProgress.question_id == question_id)
        .order_by(UserProgress.attempted_at.desc())
        .all()
    )
    options = option_payload(question)
    option_counts = [0 for _ in options]
    students = {"correct": [], "incorrect": [], "skipped": []}
    seen = set()
    for progress, user in attempts:
        if progress.user_answer is not None:
            try:
                index = int(progress.user_answer)
                if 0 <= index < len(option_counts):
                    option_counts[index] += 1
            except ValueError:
                pass
        if progress.user_id in seen:
            continue
        seen.add(progress.user_id)
        key = "correct" if progress.is_correct == "CORRECT" else "skipped" if progress.is_correct == "SKIP" else "incorrect"
        students[key].append({
            "id": user.id if user else progress.user_id,
            "name": user.name if user else f"학생 {progress.user_id}",
            "answer": progress.user_answer,
            "elapsed_seconds": round(float(progress.elapsed_seconds or 0), 1),
        })
    return {
        "question": {
            "id": question.id,
            "number": question_label(question),
            "title": question.title,
            "content": question.content,
            "explanation": question.explanation,
            "correct_option": correct_index(question),
        },
        "options": [{"index": index, "text": str(text), "count": option_counts[index]} for index, text in enumerate(options)],
        "students": students,
    }


def correct_index(question: Question):
    if question.correct_option is not None and question.correct_option >= 1:
        return question.correct_option - 1
    try:
        return int(str(question.correct_answer).strip())
    except (TypeError, ValueError):
        return None


def normalized_answer(value):
    if value is None:
        return None
    return str(value).strip().replace("\r\n", "\n")


def has_options(question: Question):
    if not question.options:
        return False
    try:
        options = json.loads(question.options)
        return isinstance(options, list) and any(str(option).strip() for option in options)
    except (TypeError, ValueError):
        return bool(str(question.options).strip())


async def grade_answer(
    question: Question,
    answer,
    db: Session | None = None,
    current_user: User | None = None,
):
    if question.answer_type == AnswerType.CODE_INPUT:
        submitted = normalized_answer(answer)
        if not submitted:
            return False, "제출된 코드가 없습니다."
        result = await tracked_code_review(db, current_user, question, submitted)
        return result["is_correct"], result["explanation"]

    if has_options(question):
        return answer is not None and answer == correct_index(question), None

    submitted = normalized_answer(answer)
    if not submitted:
        return False, None
    accepted_answers = {
        normalized_answer(question.correct_answer),
        normalized_answer(question.answer_code_snippet),
    }
    accepted_answers.discard(None)
    accepted_answers.discard("")
    if submitted in accepted_answers:
        return True, "모범 답안과 일치합니다."
    if normalized_answer(question.answer_code_snippet):
        result = await tracked_code_review(db, current_user, question, submitted)
        return result["is_correct"], result["explanation"]
    return False, None


async def tracked_code_review(
    db: Session | None,
    current_user: User | None,
    question: Question,
    submitted: str,
):
    if db is None or current_user is None:
        raise RuntimeError("AI 코드 채점에는 사용자와 DB 세션이 필요합니다.")
    from services.ai_usage import complete_ai_usage, reserve_ai_usage
    from services.answer_enrichment import grade_code_answer

    usage_db = SessionLocal()
    usage_event = None
    try:
        usage_event = reserve_ai_usage(usage_db, current_user, "CODE_REVIEW")
        result = await grade_code_answer(question, submitted)
    except Exception:
        if usage_event is not None:
            complete_ai_usage(
                usage_db,
                usage_event,
                succeeded=False,
                failure_code="CODE_REVIEW_ERROR",
            )
        raise
    else:
        succeeded = result.get("ai_succeeded", True)
        complete_ai_usage(
            usage_db,
            usage_event,
            succeeded=succeeded,
            usage=result.get("usage"),
            failure_code=None if succeeded else "CODE_REVIEW_FAILED",
        )
        return result
    finally:
        usage_db.close()


def achievement_score(question: Question, is_correct: bool, elapsed_seconds: float):
    if not is_correct:
        return 0.0
    difficulty_weight = {
        DifficultyLevel.EASY: 1.0,
        DifficultyLevel.MEDIUM: 1.2,
        DifficultyLevel.HARD: 1.5,
        DifficultyLevel.EXPERT: 1.8,
    }.get(question.difficulty, 1.0)
    benchmark = float(question.benchmark_time or 60)
    safe_elapsed = max(float(elapsed_seconds), 1.0)
    speed_weight = min(1.25, max(0.75, benchmark / safe_elapsed))
    return round(100 * difficulty_weight * speed_weight, 2)


@router.post("/submit", response_model=QuizSubmissionResult)
async def submit_quiz(
    payload: QuizSubmission,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles(UserRole.STUDENT)),
):
    if not payload.answers:
        raise HTTPException(status_code=400, detail="제출할 답안이 없습니다.")

    question_ids = list({answer.question_id for answer in payload.answers})
    questions = {
        question.id: question
        for question in scope_questions(
            db.query(Question).filter(Question.id.in_(question_ids)), current_user
        ).all()
    }
    if len(questions) != len(question_ids):
        raise HTTPException(status_code=404, detail="존재하지 않는 문제가 포함되어 있습니다.")

    correct_count = 0
    achievement_total = 0.0
    grading_results = []
    session_id = payload.session_id or str(uuid4())
    for answer in payload.answers:
        question = questions[answer.question_id]
        is_correct, grading_explanation = await grade_answer(
            question, answer.answer, db, current_user
        )
        grading_results.append(
            {
                "question_id": question.id,
                "is_correct": is_correct,
                "grading_explanation": grading_explanation,
            }
        )
        if is_correct:
            correct_count += 1
        item_achievement = achievement_score(
            question, is_correct, answer.elapsed_seconds
        )
        achievement_total += item_achievement
        db.add(
            UserProgress(
                user_id=str(current_user.id),
                question_id=question.id,
                user_answer=None if answer.answer is None else str(answer.answer),
                session_id=session_id,
                sequence_number=answer.sequence_number,
                elapsed_seconds=max(answer.elapsed_seconds, 0),
                achievement_score=item_achievement,
                is_correct=(
                    "CORRECT"
                    if is_correct
                    else "SKIP"
                    if answer.answer is None
                    else "INCORRECT"
                ),
            )
        )

    attempted = len(payload.answers)
    average_achievement = round(achievement_total / attempted, 2)
    db.add(
        QuizSession(
            id=session_id,
            user_id=current_user.id,
            total_seconds=max(payload.total_seconds, 0),
            total_questions=attempted,
            correct_answers=correct_count,
            score_percent=round(correct_count / attempted * 100),
            achievement_score=average_achievement,
        )
    )
    db.commit()
    return {
        "attempted": attempted,
        "correct": correct_count,
        "score_percent": round(correct_count / attempted * 100),
        "achievement_score": average_achievement,
        "session_id": session_id,
        "results": grading_results,
    }


@router.get("/student-analytics")
async def get_student_analytics(
    page: int = Query(1, ge=1),
    page_size: int = Query(5, ge=5, le=100),
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles(UserRole.PROFESSOR, UserRole.ADMIN)),
):
    correct_sum = func.sum(case((UserProgress.is_correct == "CORRECT", 1), else_=0))
    base = (
        db.query(
            User.id,
            User.name,
            User.email,
            User.affiliation,
            User.academic_year,
            User.course_name,
            func.count(UserProgress.id).label("attempted"),
            correct_sum.label("correct"),
            func.avg(UserProgress.achievement_score).label("achievement_score"),
            func.avg(UserProgress.elapsed_seconds).label("average_seconds"),
            func.max(UserProgress.attempted_at).label("last_attempted"),
        )
        .outerjoin(UserProgress, UserProgress.user_id == func.cast(User.id, String))
        .filter(User.role == UserRole.STUDENT)
        .group_by(
            User.id, User.name, User.email, User.affiliation,
            User.academic_year, User.course_name
        )
        .order_by(
            func.count(UserProgress.id).desc(),
            func.avg(UserProgress.achievement_score).desc(),
            User.name,
            User.id,
        )
    )
    if current_user.role == UserRole.PROFESSOR:
        base = base.filter(User.professor_id == current_user.id)
    total_query = db.query(func.count(User.id)).filter(User.role == UserRole.STUDENT)
    if current_user.role == UserRole.PROFESSOR:
        total_query = total_query.filter(User.professor_id == current_user.id)
    total = total_query.scalar() or 0
    rows = base.offset((page - 1) * page_size).limit(page_size).all()
    items = []
    for row in rows:
        attempted = int(row.attempted or 0)
        correct = int(row.correct or 0)
        items.append({
            "id": row.id,
            "name": row.name,
            "email": row.email,
            "affiliation": row.affiliation,
            "academic_year": row.academic_year,
            "course_name": row.course_name,
            "attempted": attempted,
            "correct": correct,
            "score_percent": round(correct / attempted * 100) if attempted else 0,
            "achievement_score": round(float(row.achievement_score or 0), 1),
            "average_seconds": round(float(row.average_seconds or 0), 1),
            "last_attempted": row.last_attempted,
        })
    return {"items": items, "total": int(total), "page": page, "page_size": page_size}


@router.get("/student-analytics/{student_id}")
async def get_student_analytics_detail(
    student_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles(UserRole.PROFESSOR, UserRole.ADMIN)),
):
    student_query = db.query(User).filter(
        User.id == student_id, User.role == UserRole.STUDENT
    )
    if current_user.role == UserRole.PROFESSOR:
        student_query = student_query.filter(User.professor_id == current_user.id)
    student = student_query.first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")

    correct_sum = func.sum(case((UserProgress.is_correct == "CORRECT", 1), else_=0))
    detail_query = (
        db.query(
            Subject.id.label("subject_id"),
            Subject.name.label("subject_name"),
            Question.difficulty.label("difficulty"),
            func.count(UserProgress.id).label("attempted"),
            correct_sum.label("correct"),
            func.avg(UserProgress.achievement_score).label("achievement_score"),
            func.avg(UserProgress.elapsed_seconds).label("average_seconds"),
        )
        .join(Question, UserProgress.question_id == Question.id)
        .join(Subject, Question.subject_id == Subject.id)
        .filter(UserProgress.user_id == str(student_id))
        .group_by(Subject.id, Subject.name, Question.difficulty)
        .order_by(Subject.name, Question.difficulty)
    )
    if current_user.role == UserRole.PROFESSOR:
        detail_query = detail_query.filter(Question.professor_id == current_user.id)
    rows = detail_query.all()
    groups = [{
        "subject_id": row.subject_id,
        "subject_name": row.subject_name,
        "difficulty": row.difficulty.value if hasattr(row.difficulty, "value") else str(row.difficulty),
        "attempted": int(row.attempted or 0),
        "correct": int(row.correct or 0),
        "score_percent": round((row.correct or 0) / row.attempted * 100),
        "achievement_score": round(float(row.achievement_score or 0), 1),
        "average_seconds": round(float(row.average_seconds or 0), 1),
    } for row in rows]
    total_attempted = sum(group["attempted"] for group in groups)
    total_correct = sum(group["correct"] for group in groups)
    weighted_achievement = sum(group["achievement_score"] * group["attempted"] for group in groups)
    weighted_seconds = sum(group["average_seconds"] * group["attempted"] for group in groups)
    session_count = db.query(func.count(QuizSession.id)).filter(QuizSession.user_id == student_id).scalar() or 0
    return {
        "student": {
            "id": student.id,
            "name": student.name,
            "email": student.email,
            "affiliation": student.affiliation,
            "academic_year": student.academic_year,
            "course_name": student.course_name,
        },
        "total_attempted": total_attempted,
        "total_correct": total_correct,
        "score_percent": round(total_correct / total_attempted * 100) if total_attempted else 0,
        "achievement_score": round(weighted_achievement / total_attempted, 1) if total_attempted else 0,
        "average_seconds": round(weighted_seconds / total_attempted, 1) if total_attempted else 0,
        "total_sessions": int(session_count),
        "groups": groups,
    }


@router.get("/dashboard")
async def get_dashboard(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles(UserRole.STUDENT)),
):
    correct_sum = func.sum(
        case((UserProgress.is_correct == "CORRECT", 1), else_=0)
    )
    rows = (
        db.query(
            Subject.id.label("subject_id"),
            Subject.name.label("subject_name"),
            Question.difficulty.label("difficulty"),
            func.count(UserProgress.id).label("attempted"),
            correct_sum.label("correct"),
            func.avg(UserProgress.achievement_score).label("achievement_score"),
            func.avg(UserProgress.elapsed_seconds).label("average_seconds"),
        )
        .join(Question, UserProgress.question_id == Question.id)
        .join(Subject, Question.subject_id == Subject.id)
        .filter(UserProgress.user_id == str(current_user.id))
        .filter(Question.professor_id == current_user.professor_id)
        .group_by(Subject.id, Subject.name, Question.difficulty)
        .order_by(Subject.name, Question.difficulty)
        .all()
    )
    groups = [
        {
            "subject_id": row.subject_id,
            "subject_name": row.subject_name,
            "difficulty": row.difficulty.value
            if hasattr(row.difficulty, "value")
            else str(row.difficulty),
            "attempted": row.attempted,
            "correct": int(row.correct or 0),
            "score_percent": round((row.correct or 0) / row.attempted * 100),
            "achievement_score": round(float(row.achievement_score or 0), 1),
            "average_seconds": round(float(row.average_seconds or 0), 1),
        }
        for row in rows
    ]
    total_attempted = sum(group["attempted"] for group in groups)
    total_correct = sum(group["correct"] for group in groups)
    return {
        "total_attempted": total_attempted,
        "total_correct": total_correct,
        "score_percent": (
            round(total_correct / total_attempted * 100) if total_attempted else 0
        ),
        "achievement_score": (
            round(
                sum(
                    group["achievement_score"] * group["attempted"]
                    for group in groups
                )
                / total_attempted,
                1,
            )
            if total_attempted
            else 0
        ),
        "groups": groups,
    }
