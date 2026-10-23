from datetime import datetime, time, timezone
from typing import Any
from zoneinfo import ZoneInfo

from fastapi import HTTPException
from sqlalchemy import func
from sqlalchemy.orm import Session

from models import AIUsageEvent, BillingPlan, User, UserRole, UserSubscription


KOREA_TZ = ZoneInfo("Asia/Seoul")
FEATURE_CODES = ("AI_EXPLANATION", "CODE_REVIEW", "QUESTION_GENERATION")
FREE_FEATURES: dict[str, dict[str, dict[str, int]]] = {
    "STUDENT": {"AI_EXPLANATION": {"daily_limit": 3}},
    "PROFESSOR": {},
}


def _role_value(user: User) -> str:
    return user.role.value if hasattr(user.role, "value") else str(user.role)


def _utc_now() -> datetime:
    return datetime.now(timezone.utc)


def _korea_day_bounds(now: datetime) -> tuple[datetime, datetime]:
    korea_now = now.astimezone(KOREA_TZ)
    day_start = datetime.combine(korea_now.date(), time.min, tzinfo=KOREA_TZ)
    next_day = datetime.combine(
        korea_now.date().fromordinal(korea_now.date().toordinal() + 1),
        time.min,
        tzinfo=KOREA_TZ,
    )
    return day_start.astimezone(timezone.utc), next_day.astimezone(timezone.utc)


def get_active_subscription(
    db: Session, user_id: int, now: datetime | None = None
) -> tuple[UserSubscription, BillingPlan] | None:
    effective_now = now or _utc_now()
    row = (
        db.query(UserSubscription, BillingPlan)
        .join(BillingPlan, BillingPlan.id == UserSubscription.plan_id)
        .filter(
            UserSubscription.user_id == user_id,
            UserSubscription.status == "ACTIVE",
            UserSubscription.current_period_start <= effective_now,
            UserSubscription.current_period_end > effective_now,
            BillingPlan.is_active.is_(True),
        )
        .order_by(UserSubscription.current_period_end.desc())
        .first()
    )
    return row


def _feature_limits(
    user: User, active: tuple[UserSubscription, BillingPlan] | None
) -> dict[str, int | None]:
    if _role_value(user) == UserRole.ADMIN.value:
        return {feature: None for feature in FEATURE_CODES}
    if active is None:
        free = FREE_FEATURES.get(_role_value(user), {})
        return {
            feature: int(policy["daily_limit"])
            for feature, policy in free.items()
            if "daily_limit" in policy
        }
    _, plan = active
    limits: dict[str, int | None] = {}
    for feature, policy in (plan.features or {}).items():
        if feature not in FEATURE_CODES or not isinstance(policy, dict):
            continue
        raw_limit = policy.get("daily_limit")
        if isinstance(raw_limit, int) and raw_limit >= 0:
            limits[feature] = raw_limit
    return limits


def _usage_counts(
    db: Session, user_id: int, now: datetime
) -> dict[str, int]:
    start, end = _korea_day_bounds(now)
    rows = (
        db.query(AIUsageEvent.feature_code, func.count(AIUsageEvent.id))
        .filter(
            AIUsageEvent.user_id == user_id,
            AIUsageEvent.status.in_(("STARTED", "SUCCEEDED")),
            AIUsageEvent.created_at >= start,
            AIUsageEvent.created_at < end,
        )
        .group_by(AIUsageEvent.feature_code)
        .all()
    )
    return {feature: int(count) for feature, count in rows}


def get_entitlement_snapshot(
    db: Session, user: User, now: datetime | None = None
) -> dict[str, Any]:
    effective_now = now or _utc_now()
    active = get_active_subscription(db, user.id, effective_now)
    limits = _feature_limits(user, active)
    usage = _usage_counts(db, user.id, effective_now)
    features: dict[str, dict[str, Any]] = {}
    for feature in FEATURE_CODES:
        limit = limits.get(feature, 0)
        used = usage.get(feature, 0)
        remaining = None if limit is None else max(limit - used, 0)
        features[feature] = {
            "daily_limit": limit,
            "used_today": used,
            "remaining_today": remaining,
            "is_available": limit is None or remaining > 0,
        }

    if active is None:
        return {
            "plan_code": "ADMIN" if _role_value(user) == UserRole.ADMIN.value else "FREE",
            "plan_name": "관리자" if _role_value(user) == UserRole.ADMIN.value else "무료",
            "subscription": None,
            "features": features,
        }

    subscription, plan = active
    return {
        "plan_code": plan.code,
        "plan_name": plan.name,
        "subscription": {
            "id": subscription.id,
            "plan_code": plan.code,
            "plan_name": plan.name,
            "status": subscription.status,
            "current_period_start": subscription.current_period_start,
            "current_period_end": subscription.current_period_end,
        },
        "features": features,
    }


def ensure_feature_available(
    db: Session, user: User, feature_code: str, now: datetime | None = None
) -> dict[str, Any]:
    if feature_code not in FEATURE_CODES:
        raise ValueError(f"지원하지 않는 기능 코드입니다: {feature_code}")
    entitlement = get_entitlement_snapshot(db, user, now)["features"][feature_code]
    if entitlement["daily_limit"] == 0:
        raise HTTPException(
            status_code=403,
            detail={"code": "FEATURE_NOT_INCLUDED", "message": "현재 요금제에서 사용할 수 없는 기능입니다."},
        )
    if not entitlement["is_available"]:
        raise HTTPException(
            status_code=429,
            detail={"code": "DAILY_LIMIT_EXCEEDED", "message": "오늘의 AI 사용 한도를 모두 사용했습니다."},
        )
    return entitlement
