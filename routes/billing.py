from fastapi import APIRouter, Depends, Header, HTTPException, Query, status
import hmac
from sqlalchemy.orm import Session
from typing import Literal
from datetime import datetime, timedelta, timezone

from models import BillingPlan, PaymentOrder, PaymentTransaction, User, UserRole, get_db
from schemas.billing import (
    AdminPaymentActionResponse,
    AdminAIUsageResponse,
    AdminSubscriptionResponse,
    AdminWebhookEventResponse,
    AdminRefundRequest,
    AdminPaymentResponse,
    RefundDecisionRequest,
    RefundRequestCreate,
    RefundRequestResponse,
    BillingPlanResponse,
    BillingMeResponse,
    PaymentConfirmRequest,
    PaymentConfirmResponse,
    PaymentHistoryResponse,
    PaymentOrderCreate,
    PaymentOrderResponse,
    PaymentWebhookResponse,
    SubscriptionExpiryResponse,
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
from services.refund_policy import evaluate_refund_policy
from services.refund_requests import (
    create_refund_request,
    decide_refund_request,
    list_refund_requests,
    refund_request_response,
)
from services.payment_webhooks import (
    list_admin_webhook_events,
    process_toss_payment_webhook,
    retry_failed_webhook_event,
    webhook_event_response,
)
from services.ai_usage_analytics import get_admin_ai_usage
from services.subscriptions import expire_due_subscriptions, list_admin_subscriptions
from services.toss_payments import TossPaymentError
from config import settings


router = APIRouter()


def verify_cron_authorization(authorization: str | None) -> None:
    cron_secret = settings.CRON_SECRET.strip()
    if not cron_secret:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="CRON_SECRET이 설정되지 않았습니다.",
        )
    expected = f"Bearer {cron_secret}"
    if authorization is None or not hmac.compare_digest(authorization, expected):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="유효하지 않은 스케줄 요청입니다.",
        )


@router.get("/cron/subscriptions/expire", response_model=SubscriptionExpiryResponse)
def automatically_expire_subscriptions(
    authorization: str | None = Header(default=None),
    db: Session = Depends(get_db),
):
    verify_cron_authorization(authorization)
    expired_count = expire_due_subscriptions(db)
    return {
        "expired_count": expired_count,
        "message": f"기간이 종료된 이용권 {expired_count}건을 자동 만료 처리했습니다.",
    }


@router.get("/admin/webhooks", response_model=list[AdminWebhookEventResponse])
def get_admin_webhook_events(
    event_status: Literal["RECEIVED", "PROCESSED", "FAILED"] | None = Query(default=None, alias="status"),
    limit: int = Query(default=100, ge=1, le=200),
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles(UserRole.ADMIN)),
):
    return list_admin_webhook_events(db, event_status=event_status, limit=limit)


@router.post("/admin/webhooks/{event_id}/retry", response_model=AdminWebhookEventResponse)
def retry_admin_webhook_event(
    event_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles(UserRole.ADMIN)),
    toss_client: TossPaymentsClient = Depends(get_toss_client),
):
    try:
        event = retry_failed_webhook_event(
            db, event_id=event_id, toss_client=toss_client
        )
    except TossPaymentError as exc:
        raise HTTPException(
            status_code=503 if exc.status_code >= 500 else 400,
            detail={"code": exc.code, "message": exc.message},
        ) from exc
    return webhook_event_response(event)


@router.get("/admin/ai-usage", response_model=AdminAIUsageResponse)
def get_admin_ai_usage_report(
    days: int = Query(default=30, ge=1, le=90),
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles(UserRole.ADMIN)),
):
    return get_admin_ai_usage(db, days=days)


@router.get("/admin/subscriptions", response_model=list[AdminSubscriptionResponse])
def get_admin_subscriptions(
    subscription_status: Literal["PENDING", "ACTIVE", "PAST_DUE", "CANCELED", "EXPIRED"] | None = Query(default=None, alias="status"),
    limit: int = Query(default=100, ge=1, le=200),
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles(UserRole.ADMIN)),
):
    return list_admin_subscriptions(
        db, subscription_status=subscription_status, limit=limit
    )


@router.post("/admin/subscriptions/expire", response_model=SubscriptionExpiryResponse)
def reconcile_expired_subscriptions(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles(UserRole.ADMIN)),
):
    expired_count = expire_due_subscriptions(db)
    return {
        "expired_count": expired_count,
        "message": f"기간이 종료된 이용권 {expired_count}건을 만료 처리했습니다.",
    }


@router.post("/webhooks/toss", response_model=PaymentWebhookResponse)
def receive_toss_payment_webhook(
    payload: dict,
    transmission_id: str | None = Header(default=None, alias="tosspayments-webhook-transmission-id"),
    db: Session = Depends(get_db),
    toss_client: TossPaymentsClient = Depends(get_toss_client),
):
    try:
        event, duplicate = process_toss_payment_webhook(
            db,
            payload=payload,
            transmission_id=transmission_id,
            toss_client=toss_client,
        )
    except TossPaymentError as exc:
        raise HTTPException(
            status_code=503 if exc.status_code >= 500 else 400,
            detail={"code": exc.code, "message": exc.message},
        ) from exc
    return {"event_id": event.event_id, "status": event.status, "duplicate": duplicate}


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


@router.post("/refund-requests", response_model=RefundRequestResponse, status_code=status.HTTP_201_CREATED)
def request_refund(
    payload: RefundRequestCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    refund_request = create_refund_request(
        db, current_user, order_id=payload.order_id, reason=payload.reason
    )
    order = db.query(PaymentOrder).filter(PaymentOrder.id == refund_request.order_id).one()
    return refund_request_response(refund_request, order, current_user)


@router.get("/refund-requests", response_model=list[RefundRequestResponse])
def list_my_refund_requests(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return [
        refund_request_response(request, order, user)
        for request, order, user in list_refund_requests(db, user_id=current_user.id)
    ]


@router.get("/admin/refund-requests", response_model=list[RefundRequestResponse])
def list_admin_refund_requests(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles(UserRole.ADMIN)),
):
    return [
        refund_request_response(request, order, user)
        for request, order, user in list_refund_requests(db)
    ]


@router.post("/admin/refund-requests/{request_id}/approve", response_model=RefundRequestResponse)
def approve_refund_request(
    request_id: int,
    payload: RefundDecisionRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles(UserRole.ADMIN)),
    toss_client: TossPaymentsClient = Depends(get_toss_client),
):
    request = decide_refund_request(
        db, request_id=request_id, reviewer=current_user, approved=True,
        reason=payload.reason, toss_client=toss_client,
    )
    order = db.query(PaymentOrder).filter(PaymentOrder.id == request.order_id).one()
    user = db.query(User).filter(User.id == request.user_id).one()
    return refund_request_response(request, order, user)


@router.post("/admin/refund-requests/{request_id}/reject", response_model=RefundRequestResponse)
def reject_refund_request(
    request_id: int,
    payload: RefundDecisionRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles(UserRole.ADMIN)),
):
    request = decide_refund_request(
        db, request_id=request_id, reviewer=current_user, approved=False,
        reason=payload.reason,
    )
    order = db.query(PaymentOrder).filter(PaymentOrder.id == request.order_id).one()
    user = db.query(User).filter(User.id == request.user_id).one()
    return refund_request_response(request, order, user)


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
    refund_policies = {
        order.id: evaluate_refund_policy(db, order)
        for order, _ in rows
    }
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
            "standard_full_refund": refund_policies[order.id]["standard_full_refund"],
            "requires_manual_review": refund_policies[order.id]["requires_manual_review"],
            "paid_feature_usage_count": refund_policies[order.id]["paid_feature_usage_count"],
            "refund_policy_message": refund_policies[order.id]["message"],
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
