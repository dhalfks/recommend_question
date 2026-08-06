import math
import random
from collections import defaultdict
from sqlalchemy import func
from sqlalchemy.orm import Session, aliased, joinedload

from models import DifficultyLevel, Question, User, UserProgress


DIFFICULTY_LEVEL = {
    DifficultyLevel.EASY: 0,
    DifficultyLevel.MEDIUM: 1,
    DifficultyLevel.HARD: 2,
    DifficultyLevel.EXPERT: 3,
}


def _latest_attempts(
    db: Session, professor_id: int | None = None
) -> dict[str, dict[int, UserProgress]]:
    query = db.query(
        UserProgress,
        func.row_number().over(
            partition_by=(UserProgress.user_id, UserProgress.question_id),
            order_by=(UserProgress.attempted_at.desc(), UserProgress.id.desc()),
        ).label("latest_rank"),
    )
    if professor_id is not None:
        student_ids = [
            str(row[0])
            for row in db.query(User.id).filter(User.professor_id == professor_id).all()
        ]
        if not student_ids:
            return {}
        query = query.filter(UserProgress.user_id.in_(student_ids))
    ranked = query.subquery()
    latest_attempt = aliased(UserProgress, ranked)
    attempts = db.query(latest_attempt).filter(ranked.c.latest_rank == 1).all()
    latest: dict[str, dict[int, UserProgress]] = defaultdict(dict)
    for attempt in attempts:
        latest[str(attempt.user_id)][attempt.question_id] = attempt
    return latest


def _latest_user_attempts(
    db: Session, user_id: int
) -> dict[int, UserProgress]:
    ranked = db.query(
        UserProgress,
        func.row_number().over(
            partition_by=UserProgress.question_id,
            order_by=(UserProgress.attempted_at.desc(), UserProgress.id.desc()),
        ).label("latest_rank"),
    ).filter(UserProgress.user_id == str(user_id)).subquery()
    latest_attempt = aliased(UserProgress, ranked)
    attempts = db.query(latest_attempt).filter(ranked.c.latest_rank == 1).all()
    return {attempt.question_id: attempt for attempt in attempts}


def _rating(attempt: UserProgress) -> float:
    if attempt.is_correct == "CORRECT":
        return 1.0
    if attempt.is_correct == "INCORRECT":
        return -1.0
    return -0.35


def _cosine_similarity(left: dict[int, UserProgress], right: dict[int, UserProgress]) -> float:
    overlap = set(left) & set(right)
    if len(overlap) < 2:
        return 0.0
    dot = sum(_rating(left[item]) * _rating(right[item]) for item in overlap)
    left_norm = math.sqrt(sum(_rating(left[item]) ** 2 for item in overlap))
    right_norm = math.sqrt(sum(_rating(right[item]) ** 2 for item in overlap))
    if not left_norm or not right_norm:
        return 0.0
    # Shrink small overlaps so two coincidental answers do not dominate.
    return dot / (left_norm * right_norm) * len(overlap) / (len(overlap) + 5)


def _target_difficulty(attempts: dict[int, UserProgress]) -> int:
    if not attempts:
        return 0
    accuracy = sum(item.is_correct == "CORRECT" for item in attempts.values()) / len(attempts)
    if accuracy >= 0.85:
        return 3
    if accuracy >= 0.65:
        return 2
    if accuracy >= 0.4:
        return 1
    return 0


def get_similar_learners_most_missed(
    db: Session,
    user_id: int,
    count: int = 5,
    subject_id: int | None = None,
    professor_id: int | None = None,
) -> list[dict]:
    """Return questions most often missed by learners similar to ``user_id``.

    Only each learner's latest attempt is considered.  A miss from a more
    similar learner contributes more to the ranking than one from a less
    similar learner, while the raw miss count and miss rate are included for
    a dashboard-friendly explanation.
    """
    all_latest = _latest_attempts(db, professor_id)
    user_attempts = all_latest.get(str(user_id), {})

    similar_learners: list[tuple[float, dict[int, UserProgress]]] = []
    for peer_id, peer_attempts in all_latest.items():
        if peer_id == str(user_id):
            continue
        similarity = _cosine_similarity(user_attempts, peer_attempts)
        if similarity > 0:
            similar_learners.append((similarity, peer_attempts))
    similar_learners.sort(key=lambda item: item[0], reverse=True)
    similar_learners = similar_learners[:20]

    if not similar_learners:
        return []

    question_query = db.query(Question).options(joinedload(Question.subject))
    if subject_id is not None:
        question_query = question_query.filter(Question.subject_id == subject_id)
    if professor_id is not None:
        question_query = question_query.filter(Question.professor_id == professor_id)
    question_map = {question.id: question for question in question_query.all()}

    stats: dict[int, dict[str, float | int]] = defaultdict(
        lambda: {
            "weighted_misses": 0.0,
            "weighted_attempts": 0.0,
            "miss_count": 0,
            "attempt_count": 0,
        }
    )
    for similarity, peer_attempts in similar_learners:
        for question_id, attempt in peer_attempts.items():
            if question_id not in question_map:
                continue
            stats[question_id]["weighted_attempts"] += similarity
            stats[question_id]["attempt_count"] += 1
            if attempt.is_correct != "CORRECT":
                stats[question_id]["weighted_misses"] += similarity
                stats[question_id]["miss_count"] += 1

    ranked = []
    for question_id, item in stats.items():
        if not item["miss_count"]:
            continue
        question = question_map[question_id]
        miss_rate = item["miss_count"] / item["attempt_count"] * 100
        ranked.append((
            item["weighted_misses"],
            item["miss_count"],
            miss_rate,
            question_id,
            {
                "question_id": question.id,
                "title": question.title,
                "subject_id": question.subject_id,
                "subject_name": question.subject.name if question.subject else "",
                "subject_unit": question.subject_unit or question.title,
                "difficulty": (
                    question.difficulty.value
                    if hasattr(question.difficulty, "value")
                    else str(question.difficulty)
                ),
                "similar_learner_miss_count": item["miss_count"],
                "similar_learner_attempt_count": item["attempt_count"],
                "miss_rate": round(miss_rate, 1),
                "weighted_miss_score": round(item["weighted_misses"], 3),
            },
        ))

    ranked.sort(key=lambda item: (-item[0], -item[1], -item[2], item[3]))
    return [item[-1] for item in ranked[:count]]


def get_similar_learners_most_missed_units(
    db: Session,
    user_id: int,
    count: int = 5,
    subject_id: int | None = None,
    professor_id: int | None = None,
) -> list[dict]:
    """Group similar learners' most-missed questions by subject unit."""
    questions = get_similar_learners_most_missed(
        db, user_id, count=1000, subject_id=subject_id, professor_id=professor_id
    )
    grouped: dict[tuple[int, str], dict] = {}
    for item in questions:
        unit = (item["subject_unit"] or item["title"] or "미분류").strip()
        key = (item["subject_id"], unit)
        group = grouped.setdefault(key, {
            "subject_id": item["subject_id"],
            "subject_name": item["subject_name"],
            "subject_unit": unit,
            "question_count": 0,
            "similar_learner_miss_count": 0,
            "similar_learner_attempt_count": 0,
            "weighted_miss_score": 0.0,
        })
        group["question_count"] += 1
        group["similar_learner_miss_count"] += item["similar_learner_miss_count"]
        group["similar_learner_attempt_count"] += item["similar_learner_attempt_count"]
        group["weighted_miss_score"] += item["weighted_miss_score"]

    for group in grouped.values():
        attempts = group["similar_learner_attempt_count"]
        group["miss_rate"] = round(
            group["similar_learner_miss_count"] / attempts * 100, 1
        ) if attempts else 0
        group["weighted_miss_score"] = round(group["weighted_miss_score"], 3)
    ranked = sorted(
        grouped.values(),
        key=lambda item: (-item["weighted_miss_score"], -item["miss_rate"], item["subject_unit"]),
    )
    return ranked[:count]


def get_my_latest_wrong_questions(
    db: Session,
    user_id: int,
    count: int = 5,
    professor_id: int | None = None,
) -> list[dict]:
    """Return questions whose latest attempt by the learner is not correct."""
    attempts = _latest_user_attempts(db, user_id)
    wrong = [attempt for attempt in attempts.values() if attempt.is_correct != "CORRECT"]
    wrong.sort(key=lambda attempt: (attempt.attempted_at, attempt.id), reverse=True)
    question_ids = [attempt.question_id for attempt in wrong[:count]]
    question_map = {
        question.id: question
        for question in db.query(Question)
        .options(joinedload(Question.subject))
        .filter(
            Question.id.in_(question_ids),
            Question.professor_id == professor_id,
        ).all()
    } if question_ids else {}
    items = []
    for attempt in wrong[:count]:
        question = question_map.get(attempt.question_id)
        if not question:
            continue
        items.append({
            "question_id": question.id,
            "title": question.title,
            "subject_id": question.subject_id,
            "subject_name": question.subject.name if question.subject else "",
            "subject_unit": question.subject_unit or question.title,
            "difficulty": question.difficulty.value if hasattr(question.difficulty, "value") else str(question.difficulty),
            "last_answer": attempt.user_answer,
            "last_attempted_at": attempt.attempted_at,
        })
    return items


def recommend_questions(
    db: Session,
    user_id: int,
    count: int = 5,
    subject_id: int | None = None,
    professor_id: int | None = None,
) -> tuple[list[Question], list[dict]]:
    """Hybrid user-CF + item similarity + adaptive-difficulty recommender."""
    all_latest = _latest_attempts(db, professor_id)
    user_attempts = all_latest.get(str(user_id), {})
    questions = db.query(Question)
    if subject_id:
        questions = questions.filter(Question.subject_id == subject_id)
    if professor_id is not None:
        questions = questions.filter(Question.professor_id == professor_id)
    candidates = questions.all()
    if not candidates:
        return [], []

    similarities = []
    for peer_id, peer_attempts in all_latest.items():
        if peer_id == str(user_id):
            continue
        similarity = _cosine_similarity(user_attempts, peer_attempts)
        if similarity > 0:
            similarities.append((similarity, peer_attempts))
    similarities.sort(key=lambda item: item[0], reverse=True)
    similarities = similarities[:20]

    target_level = _target_difficulty(user_attempts)
    wrong_questions = {
        question_id for question_id, attempt in user_attempts.items()
        if attempt.is_correct != "CORRECT"
    }
    question_map_query = db.query(Question)
    if professor_id is not None:
        question_map_query = question_map_query.filter(
            Question.professor_id == professor_id
        )
    question_map = {question.id: question for question in question_map_query.all()}
    weak_subjects: dict[int, float] = defaultdict(float)
    weak_tags: dict[str, float] = defaultdict(float)
    for question_id in wrong_questions:
        question = question_map.get(question_id)
        if not question:
            continue
        weak_subjects[question.subject_id] += 1
        for tag in (question.tags or "").split(','):
            if tag.strip():
                weak_tags[tag.strip().lower()] += 1

    scored = []
    for question in candidates:
        peer_numerator = 0.0
        peer_weight = 0.0
        for similarity, peer_attempts in similarities:
            peer = peer_attempts.get(question.id)
            if peer:
                peer_numerator += similarity * _rating(peer)
                peer_weight += abs(similarity)
        cf_score = peer_numerator / peer_weight if peer_weight else 0.0

        item_score = min(1.0, weak_subjects.get(question.subject_id, 0) / 3) * 0.7
        tags = {tag.strip().lower() for tag in (question.tags or "").split(',') if tag.strip()}
        if tags:
            item_score += min(0.3, sum(weak_tags.get(tag, 0) for tag in tags) * 0.1)
        level = DIFFICULTY_LEVEL.get(question.difficulty, 1)
        adaptive_score = max(0.0, 1 - abs(level - target_level) * 0.35)
        prior = user_attempts.get(question.id)
        novelty_score = 1.0 if prior is None else 0.55 if prior.is_correct != "CORRECT" else -0.8
        exploration = random.random() * 0.08
        score = cf_score * 0.38 + item_score * 0.27 + adaptive_score * 0.20 + novelty_score * 0.15 + exploration
        reasons = []
        if cf_score > 0.2:
            reasons.append("유사 학습자 추천")
        if item_score > 0.25:
            reasons.append("취약 영역 보완")
        if prior and prior.is_correct != "CORRECT":
            reasons.append("오답 복습")
        elif prior is None:
            reasons.append("새로운 문항")
        reasons.append("현재 수준에 맞는 난이도")
        scored.append((score, question, reasons))

    scored.sort(key=lambda item: item[0], reverse=True)
    selected = scored[:min(count, len(scored))]
    metadata = [
        {"question_id": question.id, "score": round(score, 3), "reasons": reasons}
        for score, question, reasons in selected
    ]
    return [question for _, question, _ in selected], metadata
