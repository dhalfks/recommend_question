import hashlib
import uuid
from datetime import datetime, timedelta, timezone
from typing import Any

from fastapi import HTTPException
from sqlalchemy.orm import Session

from models import (
    BillingPlan,
    BillingCustomer,
    PaymentOrder,
    PaymentTransaction,
    User,
    UserRole,
    UserSubscription,
)
from services.toss_payments import TossPaymentError, TossPaymentsClient


UNPAID_ORDER_CLOSE_AFTER = timedelta(minutes=30)


def _role_value(user: User) -> str:
    return user.role.value if hasattr(user.role, "value") else str(user.role)


def create_payment_order(db: Session, user: User, plan_code: str) -> PaymentOrder:
    normalized_code = plan_code.strip().upper()
    plan = (
        db.query(BillingPlan)
        .filter(BillingPlan.code == normalized_code, BillingPlan.is_active.is_(True))
        .first()
    )
    if plan is None:
        raise HTTPException(status_code=404, detail="구매 가능한 상품을 찾을 수 없습니다.")
    if _role_value(user) != plan.audience_role:
        raise HTTPException(status_code=403, detail="현재 계정 역할로 구매할 수 없는 상품입니다.")

    # Serialize first customer-key creation for the same user.
    db.query(User).filter(User.id == user.id).with_for_update().one()
    billing_customer = (
        db.query(BillingCustomer).filter(BillingCustomer.user_id == user.id).first()
    )
    if billing_customer is None:
        billing_customer = BillingCustomer(
            user_id=user.id,
            customer_key=str(uuid.uuid4()),
        )
        db.add(billing_customer)

    order = PaymentOrder(
        order_id=f"qb_{uuid.uuid4().hex}",
        user_id=user.id,
        plan_id=plan.id,
        plan_code=plan.code,
        plan_name=plan.name,
        amount=plan.price,
        currency=plan.currency,
        status="READY",
        provider="TOSS",
    )
    order.billing_customer = billing_customer
    db.add(order)
    db.commit()
    db.refresh(order)
    return order


def _confirmation_key(order_id: str, payment_key: str) -> str:
    digest = hashlib.sha256(payment_key.encode()).hexdigest()[:24]
    return f"confirm:{order_id}:{digest}"


def _safe_provider_response(payment: dict[str, Any]) -> dict[str, Any]:
    return {
        key: payment.get(key)
        for key in (
            "paymentKey",
            "orderId",
            "status",
            "totalAmount",
            "balanceAmount",
            "method",
            "requestedAt",
            "approvedAt",
        )
        if payment.get(key) is not None
    }


def _validate_toss_payment(
    payment: dict[str, Any], *, payment_key: str, order_id: str, amount: int
) -> None:
    valid = (
        payment.get("paymentKey") == payment_key
        and payment.get("orderId") == order_id
        and payment.get("totalAmount") == amount
        and payment.get("status") == "DONE"
    )
    if not valid:
        raise TossPaymentError(
            502,
            "TOSS_PAYMENT_MISMATCH",
            "토스 결제 정보가 서버 주문과 일치하지 않습니다.",
        )


def _activate_subscription(
    db: Session, order: PaymentOrder, plan: BillingPlan, now: datetime
) -> UserSubscription:
    subscription = (
        db.query(UserSubscription)
        .filter(
            UserSubscription.user_id == order.user_id,
            UserSubscription.plan_id == order.plan_id,
            UserSubscription.status == "ACTIVE",
        )
        .with_for_update()
        .first()
    )
    if subscription is None:
        subscription = UserSubscription(
            user_id=order.user_id,
            plan_id=order.plan_id,
            status="ACTIVE",
            started_at=now,
            current_period_start=now,
            current_period_end=now + timedelta(days=plan.entitlement_days),
        )
        db.add(subscription)
        db.flush()
        return subscription

    period_end = subscription.current_period_end
    if period_end is not None and period_end.tzinfo is None:
        period_end = period_end.replace(tzinfo=timezone.utc)
    extension_start = max(period_end or now, now)
    subscription.current_period_end = extension_start + timedelta(days=plan.entitlement_days)
    subscription.cancel_at_period_end = False
    subscription.canceled_at = None
    return subscription


def confirm_payment(
    db: Session,
    user: User,
    *,
    payment_key: str,
    order_id: str,
    amount: int,
    toss_client: TossPaymentsClient,
) -> tuple[PaymentOrder, UserSubscription, BillingPlan]:
    order = (
        db.query(PaymentOrder)
        .filter(PaymentOrder.order_id == order_id, PaymentOrder.user_id == user.id)
        .with_for_update()
        .first()
    )
    if order is None:
        raise HTTPException(status_code=404, detail="결제 주문을 찾을 수 없습니다.")
    plan = db.query(BillingPlan).filter(BillingPlan.id == order.plan_id).first()
    if plan is None:
        raise HTTPException(status_code=409, detail="주문 상품을 찾을 수 없습니다.")
    if order.status == "PAID" and order.subscription_id is not None:
        successful_transaction = db.query(PaymentTransaction).filter(
            PaymentTransaction.payment_order_id == order.id,
            PaymentTransaction.transaction_type == "PAYMENT",
            PaymentTransaction.status == "SUCCEEDED",
        ).first()
        if (
            successful_transaction is None
            or successful_transaction.provider_payment_id != payment_key
        ):
            raise HTTPException(status_code=409, detail="이미 다른 결제로 승인된 주문입니다.")
        subscription = db.query(UserSubscription).filter(
            UserSubscription.id == order.subscription_id
        ).first()
        if subscription is not None:
            return order, subscription, plan
    if order.status != "READY":
        raise HTTPException(status_code=409, detail="결제할 수 없는 주문 상태입니다.")
    if amount != order.amount:
        raise HTTPException(status_code=400, detail="결제 금액이 주문 금액과 일치하지 않습니다.")

    if not plan.is_active:
        raise HTTPException(status_code=409, detail="현재 구매할 수 없는 상품입니다.")
    if _role_value(user) != plan.audience_role:
        raise HTTPException(status_code=403, detail="현재 계정 역할로 구매할 수 없는 상품입니다.")

    idempotency_key = _confirmation_key(order.order_id, payment_key)
    transaction = db.query(PaymentTransaction).filter(
        PaymentTransaction.idempotency_key == idempotency_key
    ).first()
    if transaction is None:
        transaction = PaymentTransaction(
            payment_order_id=order.id,
            provider_payment_id=payment_key,
            transaction_type="PAYMENT",
            status="PENDING",
            amount=order.amount,
            currency=order.currency,
            idempotency_key=idempotency_key,
        )
        db.add(transaction)
    else:
        transaction.status = "PENDING"
        transaction.failure_code = None
        transaction.failure_message = None

    try:
        payment = toss_client.confirm_payment(
            payment_key=payment_key,
            order_id=order.order_id,
            amount=order.amount,
            idempotency_key=idempotency_key,
        )
        _validate_toss_payment(
            payment,
            payment_key=payment_key,
            order_id=order.order_id,
            amount=order.amount,
        )
    except TossPaymentError as exc:
        transaction.status = "FAILED"
        transaction.failure_code = exc.code
        transaction.failure_message = exc.message[:2000]
        order.failure_code = exc.code
        order.failure_message = exc.message[:2000]
        if exc.status_code < 500:
            order.status = "FAILED"
        db.commit()
        raise HTTPException(
            status_code=502 if exc.status_code >= 500 else 400,
            detail={"code": exc.code, "message": exc.message},
        ) from exc

    now = datetime.now(timezone.utc)
    transaction.status = "SUCCEEDED"
    transaction.provider_response = _safe_provider_response(payment)
    subscription = _activate_subscription(db, order, plan, now)
    order.subscription_id = subscription.id
    order.status = "PAID"
    order.paid_at = now
    order.failure_code = None
    order.failure_message = None
    db.commit()
    db.refresh(order)
    db.refresh(subscription)
    return order, subscription, plan


def close_unpaid_order(
    db: Session,
    *,
    order_id: str,
    now: datetime | None = None,
) -> PaymentOrder:
    effective_now = now or datetime.now(timezone.utc)
    order = (
        db.query(PaymentOrder)
        .filter(PaymentOrder.order_id == order_id)
        .with_for_update()
        .first()
    )
    if order is None:
        raise HTTPException(status_code=404, detail="결제 주문을 찾을 수 없습니다.")
    if order.status != "READY":
        raise HTTPException(status_code=409, detail="결제 대기 주문만 종료할 수 있습니다.")

    created_at = order.created_at
    if created_at.tzinfo is None:
        created_at = created_at.replace(tzinfo=timezone.utc)
    if effective_now - created_at < UNPAID_ORDER_CLOSE_AFTER:
        raise HTTPException(status_code=409, detail="생성 후 30분이 지난 주문만 종료할 수 있습니다.")

    payment_attempt = (
        db.query(PaymentTransaction)
        .filter(
            PaymentTransaction.payment_order_id == order.id,
            PaymentTransaction.provider_payment_id.is_not(None),
        )
        .first()
    )
    if payment_attempt is not None:
        raise HTTPException(
            status_code=409,
            detail="결제키가 기록된 주문은 종료할 수 없습니다. 결제 상태 확인 및 복구를 사용해 주세요.",
        )

    order.status = "CANCELED"
    order.canceled_at = effective_now
    order.failure_code = "ADMIN_CLOSED_UNPAID"
    order.failure_message = "관리자가 장시간 미완료 주문을 종료했습니다."
    db.commit()
    db.refresh(order)
    return order


def recover_payment(
    db: Session,
    *,
    order_id: str,
    toss_client: TossPaymentsClient,
) -> tuple[PaymentOrder, UserSubscription, BillingPlan]:
    order = (
        db.query(PaymentOrder)
        .filter(PaymentOrder.order_id == order_id)
        .with_for_update()
        .first()
    )
    if order is None:
        raise HTTPException(status_code=404, detail="결제 주문을 찾을 수 없습니다.")
    if order.status != "READY":
        raise HTTPException(status_code=409, detail="결제 대기 주문만 복구할 수 있습니다.")

    transaction = (
        db.query(PaymentTransaction)
        .filter(
            PaymentTransaction.payment_order_id == order.id,
            PaymentTransaction.transaction_type == "PAYMENT",
            PaymentTransaction.status.in_(("PENDING", "FAILED")),
            PaymentTransaction.provider_payment_id.is_not(None),
        )
        .order_by(PaymentTransaction.created_at.desc(), PaymentTransaction.id.desc())
        .first()
    )
    if transaction is None:
        raise HTTPException(status_code=409, detail="복구할 결제 승인 시도가 없습니다.")
    if transaction.status == "FAILED" and transaction.failure_code != "TOSS_NETWORK_ERROR":
        raise HTTPException(status_code=409, detail="네트워크 오류로 실패한 결제만 복구할 수 있습니다.")

    user = db.query(User).filter(User.id == order.user_id).first()
    if user is None:
        raise HTTPException(status_code=409, detail="주문 사용자를 찾을 수 없습니다.")
    return confirm_payment(
        db,
        user,
        payment_key=transaction.provider_payment_id,
        order_id=order.order_id,
        amount=order.amount,
        toss_client=toss_client,
    )


def order_response(order: PaymentOrder) -> dict[str, Any]:
    billing_customer = getattr(order, "billing_customer", None)
    return {
        "order_id": order.order_id,
        "order_name": order.plan_name,
        "amount": order.amount,
        "currency": order.currency,
        "status": order.status,
        "created_at": order.created_at,
        "customer_key": billing_customer.customer_key if billing_customer else None,
    }


def subscription_response(subscription: UserSubscription, plan: BillingPlan) -> dict[str, Any]:
    return {
        "id": subscription.id,
        "plan_code": plan.code,
        "plan_name": plan.name,
        "status": subscription.status,
        "current_period_start": subscription.current_period_start,
        "current_period_end": subscription.current_period_end,
    }
