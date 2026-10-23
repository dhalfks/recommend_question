import base64
from types import SimpleNamespace
import unittest
from unittest.mock import MagicMock, patch

from fastapi import HTTPException

from models import BillingPlan, PaymentOrder, PaymentTransaction, UserRole, UserSubscription
from services.billing import (
    _confirmation_key,
    _safe_provider_response,
    _validate_toss_payment,
    confirm_payment,
    create_payment_order,
)
from services.toss_payments import TossPaymentError, TossPaymentsClient


def query_result(value):
    query = MagicMock()
    query.filter.return_value = query
    query.with_for_update.return_value = query
    query.first.return_value = value
    return query


class PaymentOrderTests(unittest.TestCase):
    def test_order_uses_server_plan_price_and_snapshot(self):
        plan = SimpleNamespace(
            id=3,
            code="STUDENT_PRO",
            name="학생 Pro 30일 이용권",
            audience_role="STUDENT",
            price=4900,
            currency="KRW",
        )
        db = MagicMock()
        db.query.return_value.filter.return_value.first.return_value = plan
        db.refresh.side_effect = lambda order: setattr(order, "created_at", MagicMock())
        user = SimpleNamespace(id=7, role=UserRole.STUDENT)

        order = create_payment_order(db, user, "student_pro")

        self.assertEqual(order.amount, 4900)
        self.assertEqual(order.plan_code, "STUDENT_PRO")
        self.assertEqual(order.user_id, 7)
        self.assertTrue(order.order_id.startswith("qb_"))
        self.assertLessEqual(len(order.order_id), 64)
        db.commit.assert_called_once()

    def test_role_mismatch_is_rejected(self):
        plan = SimpleNamespace(audience_role="PROFESSOR")
        db = MagicMock()
        db.query.return_value.filter.return_value.first.return_value = plan
        user = SimpleNamespace(id=7, role=UserRole.STUDENT)

        with self.assertRaises(HTTPException) as raised:
            create_payment_order(db, user, "TEACHER_PRO")

        self.assertEqual(raised.exception.status_code, 403)
        db.add.assert_not_called()


class TossClientTests(unittest.TestCase):
    @patch("services.toss_payments.httpx.post")
    def test_confirm_uses_basic_auth_and_idempotency_header(self, post):
        post.return_value.is_error = False
        post.return_value.json.return_value = {"status": "DONE"}
        client = TossPaymentsClient("test_secret", "https://api.tosspayments.com")

        client.confirm_payment(
            payment_key="payment-key",
            order_id="qb_order1",
            amount=4900,
            idempotency_key="confirm-key",
        )

        headers = post.call_args.kwargs["headers"]
        expected = base64.b64encode(b"test_secret:").decode()
        self.assertEqual(headers["Authorization"], f"Basic {expected}")
        self.assertEqual(headers["Idempotency-Key"], "confirm-key")
        self.assertEqual(post.call_args.kwargs["json"]["amount"], 4900)

    def test_empty_secret_is_rejected_without_network(self):
        client = TossPaymentsClient("", "https://api.tosspayments.com")
        with self.assertRaises(TossPaymentError) as raised:
            client._authorization()
        self.assertEqual(raised.exception.code, "TOSS_NOT_CONFIGURED")


class PaymentConfirmationTests(unittest.TestCase):
    def test_toss_response_must_match_all_server_order_fields(self):
        valid = {
            "paymentKey": "pay_1",
            "orderId": "qb_order1",
            "totalAmount": 4900,
            "status": "DONE",
        }
        _validate_toss_payment(
            valid, payment_key="pay_1", order_id="qb_order1", amount=4900
        )
        for field, wrong_value in (
            ("paymentKey", "other"),
            ("orderId", "other"),
            ("totalAmount", 1),
            ("status", "READY"),
        ):
            invalid = {**valid, field: wrong_value}
            with self.assertRaises(TossPaymentError):
                _validate_toss_payment(
                    invalid, payment_key="pay_1", order_id="qb_order1", amount=4900
                )

    def test_provider_response_drops_card_and_customer_details(self):
        safe = _safe_provider_response(
            {
                "paymentKey": "pay_1",
                "orderId": "qb_order1",
                "status": "DONE",
                "totalAmount": 4900,
                "card": {"number": "1234"},
                "customerEmail": "private@example.com",
            }
        )
        self.assertNotIn("card", safe)
        self.assertNotIn("customerEmail", safe)

    def test_confirmation_activates_subscription_and_marks_order_paid(self):
        order = PaymentOrder(
            id=10,
            order_id="qb_order1",
            user_id=7,
            plan_id=3,
            plan_code="STUDENT_PRO",
            plan_name="학생 Pro 30일 이용권",
            amount=4900,
            currency="KRW",
            status="READY",
            provider="TOSS",
        )
        plan = BillingPlan(
            id=3,
            code="STUDENT_PRO",
            name="학생 Pro 30일 이용권",
            audience_role="STUDENT",
            price=4900,
            currency="KRW",
            billing_period="ONE_TIME",
            entitlement_days=30,
            features={},
            is_active=True,
        )
        db = MagicMock()
        db.query.side_effect = [
            query_result(order),
            query_result(plan),
            query_result(None),
            query_result(None),
        ]
        added = []
        db.add.side_effect = added.append

        def assign_subscription_id():
            for value in added:
                if isinstance(value, UserSubscription):
                    value.id = 20

        db.flush.side_effect = assign_subscription_id
        toss = MagicMock()
        toss.confirm_payment.return_value = {
            "paymentKey": "pay_1",
            "orderId": "qb_order1",
            "totalAmount": 4900,
            "status": "DONE",
            "method": "카드",
        }
        user = SimpleNamespace(id=7, role=UserRole.STUDENT)

        paid_order, subscription, returned_plan = confirm_payment(
            db,
            user,
            payment_key="pay_1",
            order_id="qb_order1",
            amount=4900,
            toss_client=toss,
        )

        self.assertEqual(paid_order.status, "PAID")
        self.assertEqual(paid_order.subscription_id, 20)
        self.assertEqual(subscription.status, "ACTIVE")
        self.assertEqual((subscription.current_period_end - subscription.current_period_start).days, 30)
        self.assertIs(returned_plan, plan)
        transaction = next(value for value in added if isinstance(value, PaymentTransaction))
        self.assertEqual(transaction.status, "SUCCEEDED")
        self.assertEqual(
            transaction.idempotency_key, _confirmation_key("qb_order1", "pay_1")
        )
        db.commit.assert_called_once()

    def test_client_amount_tampering_is_rejected_before_toss(self):
        order = SimpleNamespace(
            id=10,
            order_id="qb_order1",
            user_id=7,
            plan_id=3,
            subscription_id=None,
            amount=4900,
            status="READY",
        )
        plan = SimpleNamespace(id=3)
        db = MagicMock()
        db.query.side_effect = [query_result(order), query_result(plan)]
        toss = MagicMock()

        with self.assertRaises(HTTPException) as raised:
            confirm_payment(
                db,
                SimpleNamespace(id=7, role=UserRole.STUDENT),
                payment_key="pay_1",
                order_id="qb_order1",
                amount=100,
                toss_client=toss,
            )

        self.assertEqual(raised.exception.status_code, 400)
        toss.confirm_payment.assert_not_called()


if __name__ == "__main__":
    unittest.main()
