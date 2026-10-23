from datetime import datetime, timedelta, timezone
from types import SimpleNamespace
import unittest
from unittest.mock import MagicMock

from services.refund_policy import evaluate_refund_policy


NOW = datetime(2026, 10, 23, 12, 0, tzinfo=timezone.utc)


class RefundPolicyTests(unittest.TestCase):
    def evaluate(self, *, paid_days_ago: int, usage_count: int):
        db = MagicMock()
        db.query.return_value.filter.return_value.scalar.return_value = usage_count
        order = SimpleNamespace(
            status="PAID",
            paid_at=NOW - timedelta(days=paid_days_ago),
            subscription_id=10,
            user_id=7,
        )
        return evaluate_refund_policy(db, order, NOW)

    def test_unused_payment_within_seven_days_is_standard_full_refund(self):
        result = self.evaluate(paid_days_ago=6, usage_count=0)
        self.assertTrue(result["standard_full_refund"])
        self.assertFalse(result["requires_manual_review"])

    def test_paid_feature_usage_requires_manual_review(self):
        result = self.evaluate(paid_days_ago=2, usage_count=1)
        self.assertFalse(result["standard_full_refund"])
        self.assertTrue(result["requires_manual_review"])

    def test_payment_after_seven_days_requires_manual_review(self):
        result = self.evaluate(paid_days_ago=8, usage_count=0)
        self.assertFalse(result["standard_full_refund"])
        self.assertTrue(result["requires_manual_review"])


if __name__ == "__main__":
    unittest.main()
