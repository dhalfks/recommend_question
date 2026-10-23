from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session
from typing import Literal
from datetime import datetime, timedelta, timezone

from models import BillingPlan, PaymentOrder, PaymentTransaction, User, UserRole, get_db
from schemas.billing import (
    AdminPaymentActionResponse,
    AdminRefundRequest,
    AdminPaymentResponse,
    BillingPlanResponse,
    BillingMeResponse,
    PaymentConfirmRequest,
    PaymentConfirmResponse,
    PaymentHistoryResponse,
    PaymentOrderCreate,
    PaymentOrderResponse,
)
from services.billing import (
    close_unpaid_order,
    confirm_payment,
    create_payment_order,
    order_response,
    recover_payment,
    refund_payment,
    subscription_response,
)
from services.auth import get_current_user, require_roles
from services.toss_payments import TossPaymentsClient, get_toss_client
from services.entitlements import get_entitlement_snapshot


router = APIRouter()


@router.get("/plans", response_model=list[BillingPlanResponse])
async def list_billing_plans(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    query = db.query(BillingPlan).filter(BillingPlan.is_active.is_(True))
    if current_user.role in (UserRole.STUDENT, UserRole.PROFESSOR):
        query = query.filter(BillingPlan.audience_role == current_user.role.value)
    return query.order_by(BillingPlan.price, BillingPlan.id).all()


@router.post("/orders", response_model=PaymentOrderResponse, status_code=status.HTTP_201_CREATED)
def create_billing_order(
    payload: PaymentOrderCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    order = create_payment_order(db, current_user, payload.plan_code)
    return order_response(order)


@router.post("/payments/confirm", response_model=PaymentConfirmResponse)
def confirm_billing_payment(
    payload: PaymentConfirmRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    toss_client: TossPaymentsClient = Depends(get_toss_client),
):
    order, subscription, plan = confirm_payment(
        db,
        current_user,
        payment_key=payload.payment_key,
        order_id=payload.order_id,
        amount=payload.amount,
        toss_client=toss_client,
    )
    return {
        "order": order_response(order),
        "subscription": subscription_response(subscription, plan),
    }


@router.get("/me", response_model=BillingMeResponse)
def get_my_billing(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return get_entitlement_snapshot(db, current_user)


@router.get("/payments", response_model=list[PaymentHistoryResponse])
def list_my_payments(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return (
        db.query(PaymentOrder)
        .filter(PaymentOrder.user_id == current_user.id)
        .order_by(PaymentOrder.created_at.desc(), PaymentOrder.id.desc())
        .limit(50)
        .all()
    )


@router.get("/admin/payments", response_model=list[AdminPaymentResponse])
def list_admin_payments(
    payment_status: Literal["READY", "PAID", "FAILED", "CANCELED", "REFUNDED"] | None = Query(default=None, alias="status"),
    limit: int = Query(default=100, ge=1, le=200),
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles(UserRole.ADMIN)),
):
    query = db.query(PaymentOrder, User).join(User, User.id == PaymentOrder.user_id)
    if payment_status:
        query = query.filter(PaymentOrder.status == payment_status.upper())
    rows = (
        query.order_by(PaymentOrder.created_at.desc(), PaymentOrder.id.desc())
        .limit(limit)
        .all()
    )
    order_ids = [order.id for order, _ in rows]
    transactions = (
        db.query(PaymentTransaction)
        .filter(PaymentTransaction.payment_order_id.in_(order_ids))
        .order_by(PaymentTransaction.created_at.desc(), PaymentTransaction.id.desc())
        .all()
        if order_ids
        else []
    )
    latest_transactions: dict[int, PaymentTransaction] = {}
    for transaction in transactions:
        latest_transactions.setdefault(transaction.payment_order_id, transaction)
    close_before = datetime.now(timezone.utc) - timedelta(minutes=30)
    return [
        {
            "order_id": order.order_id,
            "plan_code": order.plan_code,
            "plan_name": order.plan_name,
            "amount": order.amount,
            "currency": order.currency,
            "status": order.status,
            "created_at": order.created_at,
            "paid_at": order.paid_at,
            "user_id": user.id,
            "user_name": user.name,
            "user_email": user.email,
            "user_role": user.role,
            "can_close": (
                order.status == "READY"
                and order.created_at <= close_before
                and not any(
                    transaction.payment_order_id == order.id
                    and transaction.provider_payment_id is not None
                    for transaction in transactions
                )
            ),
            "can_recover": (
                order.status == "READY"
                and order.id in latest_transactions
                and latest_transactions[order.id].provider_payment_id is not None
                and (
                    latest_transactions[order.id].status == "PENDING"
                    or (
                        latest_transactions[order.id].status == "FAILED"
                        and latest_transactions[order.id].failure_code == "TOSS_NETWORK_ERROR"
                    )
                )
            ),
        }
        for order, user in rows
    ]


@router.post("/admin/payments/{order_id}/close", response_model=AdminPaymentActionResponse)
def close_admin_unpaid_order(
    order_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles(UserRole.ADMIN)),
):
    order = close_unpaid_order(db, order_id=order_id)
    return {"order_id": order.order_id, "status": order.status, "message": "미결제 주문을 종료했습니다."}


@router.post("/admin/payments/{order_id}/recover", response_model=AdminPaymentActionResponse)
def recover_admin_payment(
    order_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles(UserRole.ADMIN)),
    toss_client: TossPaymentsClient = Depends(get_toss_client),
):
    order, _, _ = recover_payment(db, order_id=order_id, toss_client=toss_client)
    return {"order_id": order.order_id, "status": order.status, "message": "결제를 확인하고 복구했습니다."}


@router.post("/admin/payments/{order_id}/refund", response_model=AdminPaymentActionResponse)
def refund_admin_payment(
    order_id: str,
    payload: AdminRefundRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles(UserRole.ADMIN)),
    toss_client: TossPaymentsClient = Depends(get_toss_client),
):
    order = refund_payment(
        db,
        order_id=order_id,
        reason=payload.reason.strip(),
        toss_client=toss_client,
    )
    return {"order_id": order.order_id, "status": order.status, "message": "전액 환불을 완료했습니다."}
