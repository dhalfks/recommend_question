from datetime import datetime, timezone
from typing import Any

from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from models import PaymentOrder, PaymentTransaction, RefundRequest, User
from services.billing import refund_payment
from services.refund_policy import evaluate_refund_policy
from services.toss_payments import TossPaymentsClient


def create_refund_request(
    db: Session, user: User, *, order_id: str, reason: str
) -> RefundRequest:
    order = (
        db.query(PaymentOrder)
        .filter(PaymentOrder.order_id == order_id, PaymentOrder.user_id == user.id)
        .with_for_update()
        .first()
    )
    if order is None:
        raise HTTPException(status_code=404, detail="결제 주문을 찾을 수 없습니다.")
    if order.status != "PAID":
        raise HTTPException(status_code=409, detail="결제 완료 상태인 주문만 환불을 신청할 수 있습니다.")
    if db.query(RefundRequest).filter(
        RefundRequest.order_id == order.id, RefundRequest.status == "PENDING"
    ).first():
        raise HTTPException(status_code=409, detail="이미 검토 중인 환불 신청이 있습니다.")

    policy = evaluate_refund_policy(db, order)
    request = RefundRequest(
        order_id=order.id,
        user_id=user.id,
        status="PENDING",
        reason=reason.strip(),
        eligibility_snapshot=policy,
    )
    db.add(request)
    try:
        db.commit()
    except IntegrityError as exc:
        db.rollback()
        raise HTTPException(status_code=409, detail="이미 검토 중인 환불 신청이 있습니다.") from exc
    db.refresh(request)
    return request


def list_refund_requests(db: Session, *, user_id: int | None = None) -> list[tuple[RefundRequest, PaymentOrder, User]]:
    query = (
        db.query(RefundRequest, PaymentOrder, User)
        .join(PaymentOrder, PaymentOrder.id == RefundRequest.order_id)
        .join(User, User.id == RefundRequest.user_id)
    )
    if user_id is not None:
        query = query.filter(RefundRequest.user_id == user_id)
    return query.order_by(RefundRequest.requested_at.desc(), RefundRequest.id.desc()).limit(100).all()


def decide_refund_request(
    db: Session,
    *,
    request_id: int,
    reviewer: User,
    approved: bool,
    reason: str,
    toss_client: TossPaymentsClient | None = None,
) -> RefundRequest:
    request = (
        db.query(RefundRequest)
        .filter(RefundRequest.id == request_id)
        .with_for_update()
        .first()
    )
    if request is None:
        raise HTTPException(status_code=404, detail="환불 신청을 찾을 수 없습니다.")
    if request.status != "PENDING":
        raise HTTPException(status_code=409, detail="이미 처리된 환불 신청입니다.")

    if approved:
        if toss_client is None:
            raise RuntimeError("승인 처리에는 토스 결제 클라이언트가 필요합니다.")
        order = db.query(PaymentOrder).filter(PaymentOrder.id == request.order_id).first()
        if order is None:
            raise HTTPException(status_code=409, detail="환불할 주문을 찾을 수 없습니다.")
        refund_payment(
            db,
            order_id=order.order_id,
            reason=f"환불 신청 승인: {reason.strip()}",
            toss_client=toss_client,
        )
        transaction = db.query(PaymentTransaction).filter(
            PaymentTransaction.payment_order_id == order.id,
            PaymentTransaction.transaction_type == "REFUND",
            PaymentTransaction.status == "SUCCEEDED",
        ).first()
        request.refund_transaction_id = transaction.id if transaction else None
        request.status = "APPROVED"
    else:
        request.status = "REJECTED"

    now = datetime.now(timezone.utc)
    request.decision_reason = reason.strip()
    request.reviewed_by = reviewer.id
    request.reviewed_at = now
    request.updated_at = now
    db.commit()
    db.refresh(request)
    return request


def refund_request_response(
    request: RefundRequest, order: PaymentOrder, user: User
) -> dict[str, Any]:
    snapshot = request.eligibility_snapshot or {}
    return {
        "id": request.id,
        "order_id": order.order_id,
        "user_id": user.id,
        "user_name": user.name,
        "user_email": user.email,
        "plan_name": order.plan_name,
        "amount": order.amount,
        "currency": order.currency,
        "status": request.status,
        "reason": request.reason,
        "standard_full_refund": bool(snapshot.get("standard_full_refund")),
        "requires_manual_review": bool(snapshot.get("requires_manual_review")),
        "paid_feature_usage_count": int(snapshot.get("paid_feature_usage_count", 0)),
        "policy_message": snapshot.get("message", "환불 정책을 관리자에게 확인해 주세요."),
        "decision_reason": request.decision_reason,
        "requested_at": request.requested_at,
        "reviewed_at": request.reviewed_at,
    }
