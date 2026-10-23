from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session
from typing import Literal

from models import BillingPlan, PaymentOrder, User, UserRole, get_db
from schemas.billing import (
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
    confirm_payment,
    create_payment_order,
    order_response,
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
        }
        for order, user in rows
    ]
