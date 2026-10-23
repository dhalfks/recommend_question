from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from models import BillingPlan, User, UserRole, get_db
from schemas.billing import (
    BillingPlanResponse,
    PaymentConfirmRequest,
    PaymentConfirmResponse,
    PaymentOrderCreate,
    PaymentOrderResponse,
)
from services.billing import (
    confirm_payment,
    create_payment_order,
    order_response,
    subscription_response,
)
from services.auth import get_current_user
from services.toss_payments import TossPaymentsClient, get_toss_client


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
