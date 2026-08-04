"""Create ten deterministic demo students and realistic quiz histories.

Safe to run repeatedly: existing sample users and their existing histories are kept.
"""
import json
import random
from datetime import datetime, timedelta
from uuid import uuid4
from sqlalchemy import String, cast

from models import DifficultyLevel, Question, QuizSession, SessionLocal, User, UserProgress, UserRole
from services.auth import hash_password


STUDENTS = [
    ("김민준", 0.88), ("이서연", 0.80), ("박지후", 0.73), ("최하윤", 0.68),
    ("정도윤", 0.62), ("강지아", 0.57), ("조현우", 0.52), ("윤서아", 0.47),
    ("장시우", 0.42), ("임채원", 0.36),
]
DIFFICULTY_PENALTY = {
    DifficultyLevel.EASY: 0.02, DifficultyLevel.MEDIUM: 0.10,
    DifficultyLevel.HARD: 0.20, DifficultyLevel.EXPERT: 0.30,
}


def answer_index(question: Question):
    if question.correct_option is not None:
        return question.correct_option - 1
    try:
        return int(str(question.correct_answer).strip())
    except (TypeError, ValueError):
        return None


def answer_for(question: Question, correct: bool):
    try:
        options = json.loads(question.options or "[]")
    except (TypeError, ValueError):
        options = []
    correct_answer = answer_index(question)
    if options and correct_answer is not None:
        if correct:
            return str(correct_answer)
        wrong = [index for index in range(len(options)) if index != correct_answer]
        return str(random.choice(wrong)) if wrong else None
    return str(question.correct_answer or question.answer_code_snippet or "정답") if correct else "잘못된 답변"


def seed():
    random.seed(20260803)
    db = SessionLocal()
    created_users = 0
    created_attempts = 0
    try:
        questions = db.query(Question).order_by(Question.id).all()
        if len(questions) < 10:
            raise RuntimeError("샘플 풀이 기록을 만들려면 문항이 10개 이상 필요합니다.")
        # A shared pool guarantees enough co-rated items for collaborative filtering.
        shared_pool = questions[:min(80, len(questions))]
        for number, (name, skill) in enumerate(STUDENTS, start=1):
            email = f"adaptive.student{number:02d}@example.com"
            user = db.query(User).filter(User.email == email).first()
            if user is None:
                user = User(
                    name=name,
                    phone=f"010-8000-{number:04d}",
                    email=email,
                    password_hash=hash_password("Sample1234!"),
                    role=UserRole.STUDENT,
                )
                db.add(user)
                db.flush()
                created_users += 1
            if db.query(UserProgress).filter(UserProgress.user_id == str(user.id)).first():
                continue

            attempt_count = random.randint(55, min(90, len(questions)))
            shared_count = min(40, attempt_count, len(shared_pool))
            selected = random.sample(shared_pool, shared_count)
            remaining = [question for question in questions if question.id not in {item.id for item in selected}]
            selected += random.sample(remaining, attempt_count - shared_count)
            random.shuffle(selected)

            started = datetime.now() - timedelta(days=random.randint(10, 45))
            for offset in range(0, len(selected), 10):
                batch = selected[offset:offset + 10]
                session_id = str(uuid4())
                session_progress = []
                correct_count = 0
                total_seconds = 0.0
                for sequence, question in enumerate(batch, start=1):
                    probability = max(0.08, min(0.96, skill - DIFFICULTY_PENALTY.get(question.difficulty, 0.1) + random.uniform(-0.12, 0.12)))
                    skipped = random.random() < 0.035
                    correct = not skipped and random.random() < probability
                    elapsed = round(max(8, random.gauss(50 + DIFFICULTY_PENALTY.get(question.difficulty, 0.1) * 150, 18)), 1)
                    total_seconds += elapsed
                    correct_count += int(correct)
                    session_progress.append(UserProgress(
                        user_id=str(user.id), question_id=question.id,
                        is_correct="SKIP" if skipped else "CORRECT" if correct else "INCORRECT",
                        user_answer=None if skipped else answer_for(question, correct),
                        session_id=session_id, sequence_number=sequence,
                        elapsed_seconds=elapsed, achievement_score=100.0 if correct else 0.0,
                        attempted_at=started + timedelta(days=offset // 10, minutes=sequence * 2),
                    ))
                score = round(correct_count / len(batch) * 100)
                db.add(QuizSession(
                    id=session_id, user_id=user.id, total_seconds=round(total_seconds, 1),
                    total_questions=len(batch), correct_answers=correct_count,
                    score_percent=score, achievement_score=float(score),
                    completed_at=started + timedelta(days=offset // 10, hours=1),
                ))
                db.add_all(session_progress)
                created_attempts += len(session_progress)
        db.commit()
        total_samples = db.query(User).filter(User.email.like("adaptive.student%@example.com")).count()
        total_attempts = (
            db.query(UserProgress).join(User, cast(User.id, String) == UserProgress.user_id)
            .filter(User.email.like("adaptive.student%@example.com")).count()
        )
        print({"created_users": created_users, "sample_users": total_samples, "created_attempts": created_attempts, "sample_attempts": total_attempts})
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    seed()
