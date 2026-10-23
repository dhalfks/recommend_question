from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from models import BillingPlan, User, UserRole, get_db
from schemas.billing import BillingPlanResponse
from services.auth import get_current_user


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
