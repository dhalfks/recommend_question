from datetime import datetime, timedelta, timezone
from typing import Any

from sqlalchemy import case, func
from sqlalchemy.orm import Session

from config import settings
from models import AIUsageEvent, User


FEATURE_LABELS = {
    "AI_EXPLANATION": "AI 오답 해설",
    "CODE_REVIEW": "AI 코드 채점",
    "QUESTION_GENERATION": "AI 문제 생성",
}


def _cost(input_tokens: int, output_tokens: int) -> float:
    value = (
        input_tokens * settings.AI_INPUT_COST_PER_MILLION_KRW
        + output_tokens * settings.AI_OUTPUT_COST_PER_MILLION_KRW
    ) / 1_000_000
    return round(value, 2)


def _metric(key: str, label: str, row: Any) -> dict[str, Any]:
    total = int(row.total_requests or 0)
    succeeded = int(row.succeeded_requests or 0)
    failed = int(row.failed_requests or 0)
    input_tokens = int(row.input_tokens or 0)
    output_tokens = int(row.output_tokens or 0)
    return {
        "key": key,
        "label": label,
        "total_requests": total,
        "succeeded_requests": succeeded,
        "failed_requests": failed,
        "input_tokens": input_tokens,
        "output_tokens": output_tokens,
        "estimated_cost_krw": _cost(input_tokens, output_tokens),
    }


def _aggregates():
    return (
        func.count(AIUsageEvent.id).label("total_requests"),
        func.sum(case((AIUsageEvent.status == "SUCCEEDED", 1), else_=0)).label("succeeded_requests"),
        func.sum(case((AIUsageEvent.status == "FAILED", 1), else_=0)).label("failed_requests"),
        func.coalesce(func.sum(AIUsageEvent.input_tokens), 0).label("input_tokens"),
        func.coalesce(func.sum(AIUsageEvent.output_tokens), 0).label("output_tokens"),
    )


def get_admin_ai_usage(db: Session, *, days: int) -> dict[str, Any]:
    period_end = datetime.now(timezone.utc)
    period_start = period_end - timedelta(days=days)
    base_filter = AIUsageEvent.created_at >= period_start

    summary_row = db.query(*_aggregates()).filter(base_filter).one()
    feature_rows = (
        db.query(AIUsageEvent.feature_code, *_aggregates())
        .filter(base_filter)
        .group_by(AIUsageEvent.feature_code)
        .order_by(func.count(AIUsageEvent.id).desc())
        .all()
    )
    user_rows = (
        db.query(User.id, User.name, User.email, *_aggregates())
        .join(AIUsageEvent, AIUsageEvent.user_id == User.id)
        .filter(base_filter)
        .group_by(User.id, User.name, User.email)
        .order_by(func.count(AIUsageEvent.id).desc())
        .limit(20)
        .all()
    )

    return {
        "period_start": period_start,
        "period_end": period_end,
        "cost_configured": (
            settings.AI_INPUT_COST_PER_MILLION_KRW > 0
            or settings.AI_OUTPUT_COST_PER_MILLION_KRW > 0
        ),
        "summary": _metric("ALL", "전체", summary_row),
        "by_feature": [
            _metric(row.feature_code, FEATURE_LABELS.get(row.feature_code, row.feature_code), row)
            for row in feature_rows
        ],
        "by_user": [
            _metric(str(row.id), f"{row.name} ({row.email})", row)
            for row in user_rows
        ],
    }
