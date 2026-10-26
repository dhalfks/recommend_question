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
    customer_key: str | None = None


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


class PaymentHistoryResponse(BaseModel):
    order_id: str
    plan_code: str
    plan_name: str
    amount: int
    currency: Literal["KRW"]
    status: Literal["READY", "PAID", "FAILED", "CANCELED", "REFUNDED"]
    created_at: datetime
    paid_at: datetime | None = None


class AdminPaymentResponse(PaymentHistoryResponse):
    user_id: int
    user_name: str
    user_email: str
    user_role: Literal["STUDENT", "PROFESSOR", "ADMIN"]
    can_close: bool
    can_recover: bool
    standard_full_refund: bool
    requires_manual_review: bool
    paid_feature_usage_count: int
    refund_policy_message: str


class AdminPaymentActionResponse(BaseModel):
    order_id: str
    status: Literal["PAID", "CANCELED", "REFUNDED"]
    message: str


class AdminRefundRequest(BaseModel):
    reason: str = Field(min_length=2, max_length=200)


class RefundRequestCreate(BaseModel):
    order_id: str = Field(min_length=6, max_length=100)
    reason: str = Field(min_length=2, max_length=1000)


class RefundDecisionRequest(BaseModel):
    reason: str = Field(min_length=2, max_length=1000)


class RefundRequestResponse(BaseModel):
    id: int
    order_id: str
    user_id: int
    user_name: str
    user_email: str
    plan_name: str
    amount: int
    currency: Literal["KRW"]
    status: Literal["PENDING", "APPROVED", "REJECTED"]
    reason: str
    standard_full_refund: bool
    requires_manual_review: bool
    paid_feature_usage_count: int
    policy_message: str
    decision_reason: str | None = None
    requested_at: datetime
    reviewed_at: datetime | None = None


class FeatureEntitlementResponse(BaseModel):
    daily_limit: int | None
    used_today: int
    remaining_today: int | None
    is_available: bool


class BillingMeResponse(BaseModel):
    plan_code: str
    plan_name: str
    subscription: SubscriptionResponse | None = None
    features: dict[str, FeatureEntitlementResponse]


class PaymentWebhookResponse(BaseModel):
    event_id: str
    status: Literal["PROCESSED", "FAILED"]
    duplicate: bool


class AIUsageMetric(BaseModel):
    key: str
    label: str
    total_requests: int
    succeeded_requests: int
    failed_requests: int
    input_tokens: int
    output_tokens: int
    estimated_cost_krw: float


class AdminAIUsageResponse(BaseModel):
    period_start: datetime
    period_end: datetime
    cost_configured: bool
    summary: AIUsageMetric
    by_feature: list[AIUsageMetric]
    by_user: list[AIUsageMetric]
