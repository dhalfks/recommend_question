from datetime import datetime
from typing import Any, Literal

from pydantic import BaseModel, ConfigDict


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
