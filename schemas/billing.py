from datetime import datetime
from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field


AudienceRole = Literal["STUDENT", "PROFESSOR"]
BillingPeriod = Literal["ONE_TIME", "MONTHLY"]


class BillingPlanResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    code: str
    name: str
    audience_role: AudienceRole
    price: int
    currency: Literal["KRW"]
    billing_period: BillingPeriod
    entitlement_days: int
    features: dict[str, Any]
    is_active: bool
    created_at: datetime
    updated_at: datetime


class PaymentOrderCreate(BaseModel):
    plan_code: str = Field(min_length=1, max_length=50)


class PaymentOrderResponse(BaseModel):
    order_id: str
    order_name: str
    amount: int
    currency: Literal["KRW"]
    status: Literal["READY", "PAID", "FAILED", "CANCELED", "REFUNDED"]
    created_at: datetime


class PaymentConfirmRequest(BaseModel):
    payment_key: str = Field(min_length=1, max_length=200)
    order_id: str = Field(min_length=6, max_length=64)
    amount: int = Field(gt=0)


class SubscriptionResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    plan_code: str
    plan_name: str
    status: Literal["ACTIVE"]
    current_period_start: datetime
    current_period_end: datetime


class PaymentConfirmResponse(BaseModel):
    order: PaymentOrderResponse
    subscription: SubscriptionResponse
