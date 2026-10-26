import hashlib
import json
from datetime import datetime, timezone
from typing import Any

from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from models import PaymentWebhookEvent
from services.billing import reconcile_paid_payment
from services.toss_payments import TossPaymentError, TossPaymentsClient


ALLOWED_TOSS_WEBHOOK_STATUSES = {
    "READY", "IN_PROGRESS", "WAITING_FOR_DEPOSIT", "DONE", "CANCELED",
    "PARTIAL_CANCELED", "ABORTED", "EXPIRED",
}


def list_admin_webhook_events(
    db: Session, *, event_status: str | None = None, limit: int = 100
) -> list[dict[str, Any]]:
    query = db.query(PaymentWebhookEvent)
    if event_status:
        query = query.filter(PaymentWebhookEvent.status == event_status)
    events = (
        query.order_by(
            PaymentWebhookEvent.received_at.desc(), PaymentWebhookEvent.id.desc()
        )
        .limit(limit)
        .all()
    )
    return [
        {
            "id": event.id,
            "provider": event.provider,
            "event_id": event.event_id,
            "event_type": event.event_type,
            "status": event.status,
            "order_id": (event.payload or {}).get("orderId"),
            "payment_status": (event.payload or {}).get("status"),
            "error_message": event.error_message,
            "received_at": event.received_at,
            "processed_at": event.processed_at,
        }
        for event in events
    ]


def _event_id(transmission_id: str | None, payload: dict[str, Any]) -> str:
    if transmission_id and transmission_id.strip():
        return transmission_id.strip()[:200]
    canonical = json.dumps(payload, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return "derived:" + hashlib.sha256(canonical.encode()).hexdigest()


def _safe_payload(payload: dict[str, Any]) -> dict[str, Any]:
    return {
        key: payload.get(key)
        for key in ("eventType", "createdAt", "orderId", "paymentKey", "status", "transactionKey")
        if payload.get(key) is not None
    }


def process_toss_payment_webhook(
    db: Session,
    *,
    payload: dict[str, Any],
    transmission_id: str | None,
    toss_client: TossPaymentsClient,
) -> tuple[PaymentWebhookEvent, bool]:
    order_id = payload.get("orderId")
    webhook_status = payload.get("status")
    if not isinstance(order_id, str) or not order_id.strip():
        raise HTTPException(status_code=400, detail="웹훅 주문번호가 없습니다.")
    if webhook_status not in ALLOWED_TOSS_WEBHOOK_STATUSES:
        raise HTTPException(status_code=400, detail="지원하지 않는 결제 상태입니다.")

    event_id = _event_id(transmission_id, payload)
    existing = db.query(PaymentWebhookEvent).filter(
        PaymentWebhookEvent.provider == "TOSS",
        PaymentWebhookEvent.event_id == event_id,
    ).first()
    if existing is not None and existing.status == "PROCESSED":
        return existing, True

    if existing is not None:
        event = existing
        event.status = "RECEIVED"
        event.error_message = None
        event.payload = _safe_payload(payload)
        db.commit()
    else:
        event = PaymentWebhookEvent(
            provider="TOSS",
            event_id=event_id,
            event_type=str(payload.get("eventType") or "PAYMENT_STATUS_CHANGED")[:100],
            status="RECEIVED",
            payload=_safe_payload(payload),
        )
        db.add(event)
        try:
            db.commit()
        except IntegrityError:
            db.rollback()
            concurrent = db.query(PaymentWebhookEvent).filter(
                PaymentWebhookEvent.provider == "TOSS",
                PaymentWebhookEvent.event_id == event_id,
            ).one()
            if concurrent.status == "PROCESSED":
                return concurrent, True
            event = concurrent
        db.refresh(event)

    try:
        verified_payment = toss_client.get_payment_by_order_id(order_id=order_id)
        if verified_payment.get("orderId") != order_id:
            raise HTTPException(status_code=400, detail="토스 결제 주문번호가 일치하지 않습니다.")
        if verified_payment.get("status") != webhook_status:
            raise HTTPException(status_code=409, detail="웹훅과 토스 조회 상태가 일치하지 않습니다.")
        if webhook_status == "DONE":
            reconcile_paid_payment(db, order_id=order_id, payment=verified_payment)
        event.status = "PROCESSED"
        event.processed_at = datetime.now(timezone.utc)
        event.error_message = None
        db.commit()
        db.refresh(event)
        return event, False
    except (TossPaymentError, HTTPException) as exc:
        event.status = "FAILED"
        event.error_message = str(exc)[:2000]
        db.commit()
        raise
