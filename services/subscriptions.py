from datetime import datetime, timezone
from typing import Any

from sqlalchemy.orm import Session

from models import BillingPlan, User, UserSubscription


SUBSCRIPTION_STATUSES = ("PENDING", "ACTIVE", "PAST_DUE", "CANCELED", "EXPIRED")


def expire_due_subscriptions(db: Session, *, now: datetime | None = None) -> int:
    effective_now = now or datetime.now(timezone.utc)
    expired_count = (
        db.query(UserSubscription)
        .filter(
            UserSubscription.status == "ACTIVE",
            UserSubscription.current_period_end.is_not(None),
            UserSubscription.current_period_end <= effective_now,
        )
        .update(
            {
                UserSubscription.status: "EXPIRED",
                UserSubscription.updated_at: effective_now,
            },
            synchronize_session=False,
        )
    )
    db.commit()
    return int(expired_count)


def list_admin_subscriptions(
    db: Session, *, subscription_status: str | None = None, limit: int = 100
) -> list[dict[str, Any]]:
    now = datetime.now(timezone.utc)
    query = (
        db.query(UserSubscription, User, BillingPlan)
        .join(User, User.id == UserSubscription.user_id)
        .join(BillingPlan, BillingPlan.id == UserSubscription.plan_id)
    )
    if subscription_status:
        query = query.filter(UserSubscription.status == subscription_status)
    rows = query.order_by(UserSubscription.created_at.desc(), UserSubscription.id.desc()).limit(limit).all()
    result = []
    for subscription, user, plan in rows:
        period_end = subscription.current_period_end
        if period_end is not None and period_end.tzinfo is None:
            period_end = period_end.replace(tzinfo=timezone.utc)
        remaining_seconds = max((period_end - now).total_seconds(), 0) if period_end else 0
        result.append({
            "id": subscription.id,
            "user_id": user.id,
            "user_name": user.name,
            "user_email": user.email,
            "user_role": user.role,
            "plan_code": plan.code,
            "plan_name": plan.name,
            "status": subscription.status,
            "current_period_start": subscription.current_period_start,
            "current_period_end": subscription.current_period_end,
            "remaining_days": int(remaining_seconds // 86400),
            "created_at": subscription.created_at,
        })
    return result
