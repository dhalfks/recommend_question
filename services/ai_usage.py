from datetime import datetime, timezone
from typing import Any
from uuid import uuid4

from sqlalchemy import text
from sqlalchemy.orm import Session

from models import AIUsageEvent, User
from services.entitlements import ensure_feature_available, get_active_subscription


def reserve_ai_usage(
    db: Session,
    user: User,
    feature_code: str,
    request_id: str | None = None,
) -> AIUsageEvent:
    # PostgreSQL transaction advisory lock serializes quota reservations per user.
    db.execute(
        text("SELECT pg_advisory_xact_lock(:user_id)"),
        {"user_id": int(user.id)},
    )
    ensure_feature_available(db, user, feature_code)
    active = get_active_subscription(db, user.id)
    subscription_id = active[0].id if active is not None else None
    event = AIUsageEvent(
        user_id=user.id,
        feature_code=feature_code,
        subscription_id=subscription_id,
        request_id=request_id or str(uuid4()),
        status="STARTED",
    )
    db.add(event)
    db.commit()
    db.refresh(event)
    return event


def complete_ai_usage(
    db: Session,
    event: AIUsageEvent,
    *,
    succeeded: bool,
    usage: dict[str, Any] | None = None,
    failure_code: str | None = None,
) -> None:
    usage = usage or {}
    event.input_tokens = _nonnegative_int(usage.get("input_tokens"))
    event.output_tokens = _nonnegative_int(usage.get("output_tokens"))
    event.status = "SUCCEEDED" if succeeded else "FAILED"
    event.failure_code = None if succeeded else (failure_code or "AI_REQUEST_FAILED")[:100]
    event.completed_at = datetime.now(timezone.utc)
    db.commit()


def _nonnegative_int(value: Any) -> int | None:
    if value is None:
        return None
    try:
        parsed = int(value)
    except (TypeError, ValueError):
        return None
    return max(parsed, 0)
