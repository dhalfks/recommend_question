from datetime import datetime, timedelta, timezone
from typing import Any

from sqlalchemy import func
from sqlalchemy.orm import Session

from models import AIUsageEvent, PaymentOrder


REFUND_REQUEST_DAYS = 7


def evaluate_refund_policy(
    db: Session, order: PaymentOrder, now: datetime | None = None
) -> dict[str, Any]:
    effective_now = now or datetime.now(timezone.utc)
    paid_at = order.paid_at
    if paid_at is not None and paid_at.tzinfo is None:
        paid_at = paid_at.replace(tzinfo=timezone.utc)

    usage_count = 0
    if paid_at is not None and order.subscription_id is not None:
        usage_count = int(
            db.query(func.count(AIUsageEvent.id))
            .filter(
                AIUsageEvent.user_id == order.user_id,
                AIUsageEvent.subscription_id == order.subscription_id,
                AIUsageEvent.status == "SUCCEEDED",
                AIUsageEvent.created_at >= paid_at,
            )
            .scalar()
            or 0
        )

    within_seven_days = bool(
        paid_at is not None and effective_now <= paid_at + timedelta(days=REFUND_REQUEST_DAYS)
    )
    standard_full_refund = order.status == "PAID" and within_seven_days and usage_count == 0
    if standard_full_refund:
        message = "결제 후 7일 이내이며 유료 AI 기능 사용 내역이 없어 전액 환불 기준에 해당합니다."
    elif order.status != "PAID":
        message = "결제 완료 상태가 아니므로 일반 환불 대상이 아닙니다."
    elif not within_seven_days:
        message = "결제 후 7일이 지나 관리자 검토가 필요합니다."
    else:
        message = "유료 AI 기능 사용 내역이 있어 관계 법령과 이용 내역에 따른 관리자 검토가 필요합니다."
    return {
        "standard_full_refund": standard_full_refund,
        "requires_manual_review": order.status == "PAID" and not standard_full_refund,
        "paid_feature_usage_count": usage_count,
        "message": message,
    }
