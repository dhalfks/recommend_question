from datetime import datetime, timezone
from pathlib import Path
from types import SimpleNamespace
import asyncio
import unittest
from unittest.mock import MagicMock

from models import BillingPlan, UserRole
from routes.billing import list_admin_payments, list_billing_plans, list_my_payments
from schemas.billing import AdminPaymentResponse, BillingPlanResponse, PaymentHistoryResponse


ROOT = Path(__file__).resolve().parents[1]
MAIN = (ROOT / "main.py").read_text(encoding="utf-8")
ROUTE = (ROOT / "routes/billing.py").read_text(encoding="utf-8")


class BillingSchemaTests(unittest.TestCase):
    def test_plan_response_serializes_orm_attributes(self):
        now = datetime.now(timezone.utc)
        plan = SimpleNamespace(
            id=1,
            code="STUDENT_PRO",
            name="학생 Pro 30일 이용권",
            audience_role="STUDENT",
            price=4900,
            currency="KRW",
            billing_period="ONE_TIME",
            entitlement_days=30,
            features={"AI_EXPLANATION": {"daily_limit": 50}},
            is_active=True,
            created_at=now,
            updated_at=now,
        )
        response = BillingPlanResponse.model_validate(plan)
        self.assertEqual(response.price, 4900)
        self.assertEqual(response.features["AI_EXPLANATION"]["daily_limit"], 50)


class BillingRouteTests(unittest.TestCase):
    def test_student_only_queries_student_active_plans(self):
        db = MagicMock()
        query = db.query.return_value
        query.filter.return_value = query
        query.order_by.return_value = query
        query.all.return_value = []
        user = SimpleNamespace(role=UserRole.STUDENT)

        result = asyncio.run(list_billing_plans(db=db, current_user=user))

        self.assertEqual(result, [])
        db.query.assert_called_once_with(BillingPlan)
        self.assertEqual(query.filter.call_count, 2)
        query.order_by.assert_called_once()

    def test_admin_can_query_all_active_plans(self):
        db = MagicMock()
        query = db.query.return_value
        query.filter.return_value = query
        query.order_by.return_value = query
        query.all.return_value = []
        user = SimpleNamespace(role=UserRole.ADMIN)

        asyncio.run(list_billing_plans(db=db, current_user=user))

        self.assertEqual(query.filter.call_count, 1)

    def test_route_requires_authentication_and_is_registered(self):
        self.assertIn("Depends(get_current_user)", ROUTE)
        self.assertIn('prefix="/api/billing"', MAIN)
        self.assertIn('@router.get("/me", response_model=BillingMeResponse)', ROUTE)

    def test_payment_history_is_scoped_to_current_user(self):
        db = MagicMock()
        query = db.query.return_value
        query.filter.return_value = query
        query.order_by.return_value = query
        query.limit.return_value = query
        query.all.return_value = []

        result = list_my_payments(db=db, current_user=SimpleNamespace(id=42))

        self.assertEqual(result, [])
        query.filter.assert_called_once()
        query.limit.assert_called_once_with(50)

    def test_payment_history_schema_hides_provider_details(self):
        fields = PaymentHistoryResponse.model_fields
        self.assertNotIn("provider_payment_id", fields)
        self.assertNotIn("provider_response", fields)

    def test_admin_payment_history_is_limited_and_has_customer_context(self):
        db = MagicMock()
        query = db.query.return_value
        query.join.return_value = query
        query.order_by.return_value = query
        query.limit.return_value = query
        query.all.return_value = []

        result = list_admin_payments(
            payment_status=None,
            limit=100,
            db=db,
            current_user=SimpleNamespace(role=UserRole.ADMIN),
        )

        self.assertEqual(result, [])
        query.limit.assert_called_once_with(100)
        self.assertIn("user_email", AdminPaymentResponse.model_fields)
        self.assertNotIn("provider_payment_id", AdminPaymentResponse.model_fields)


if __name__ == "__main__":
    unittest.main()
