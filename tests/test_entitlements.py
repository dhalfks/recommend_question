from datetime import datetime, timezone
from types import SimpleNamespace
import unittest
from unittest.mock import MagicMock, patch

from fastapi import HTTPException

from models import UserRole
from services.entitlements import (
    _feature_limits,
    _korea_day_bounds,
    ensure_feature_available,
    get_entitlement_snapshot,
)


NOW = datetime(2026, 10, 23, 16, 30, tzinfo=timezone.utc)


class EntitlementPolicyTests(unittest.TestCase):
    def test_free_student_has_three_daily_explanations_only(self):
        user = SimpleNamespace(role=UserRole.STUDENT)
        limits = _feature_limits(user, None)
        self.assertEqual(limits, {"AI_EXPLANATION": 3})

    def test_paid_limits_come_from_plan_features(self):
        user = SimpleNamespace(role=UserRole.STUDENT)
        plan = SimpleNamespace(
            features={
                "AI_EXPLANATION": {"daily_limit": 50},
                "CODE_REVIEW": {"daily_limit": 50},
            }
        )
        limits = _feature_limits(user, (SimpleNamespace(), plan))
        self.assertEqual(limits["AI_EXPLANATION"], 50)
        self.assertEqual(limits["CODE_REVIEW"], 50)

    def test_admin_features_are_unlimited(self):
        user = SimpleNamespace(role=UserRole.ADMIN)
        limits = _feature_limits(user, None)
        self.assertTrue(all(value is None for value in limits.values()))

    def test_korea_daily_window_is_converted_to_utc(self):
        start, end = _korea_day_bounds(NOW)
        self.assertEqual(start.isoformat(), "2026-10-23T15:00:00+00:00")
        self.assertEqual(end.isoformat(), "2026-10-24T15:00:00+00:00")


class EntitlementSnapshotTests(unittest.TestCase):
    @patch("services.entitlements._usage_counts", return_value={"AI_EXPLANATION": 2})
    @patch("services.entitlements.get_active_subscription", return_value=None)
    def test_free_snapshot_reports_remaining_usage(self, active, usage):
        db = MagicMock()
        user = SimpleNamespace(id=7, role=UserRole.STUDENT)
        snapshot = get_entitlement_snapshot(db, user, NOW)
        explanation = snapshot["features"]["AI_EXPLANATION"]
        self.assertEqual(snapshot["plan_code"], "FREE")
        self.assertEqual(explanation["daily_limit"], 3)
        self.assertEqual(explanation["remaining_today"], 1)
        self.assertTrue(explanation["is_available"])

    @patch("services.entitlements._usage_counts", return_value={"AI_EXPLANATION": 3})
    @patch("services.entitlements.get_active_subscription", return_value=None)
    def test_exhausted_limit_raises_429(self, active, usage):
        db = MagicMock()
        user = SimpleNamespace(id=7, role=UserRole.STUDENT)
        with self.assertRaises(HTTPException) as raised:
            ensure_feature_available(db, user, "AI_EXPLANATION", NOW)
        self.assertEqual(raised.exception.status_code, 429)

    @patch("services.entitlements._usage_counts", return_value={})
    @patch("services.entitlements.get_active_subscription", return_value=None)
    def test_feature_not_included_raises_403(self, active, usage):
        db = MagicMock()
        user = SimpleNamespace(id=7, role=UserRole.STUDENT)
        with self.assertRaises(HTTPException) as raised:
            ensure_feature_available(db, user, "QUESTION_GENERATION", NOW)
        self.assertEqual(raised.exception.status_code, 403)

    @patch("services.entitlements._usage_counts", return_value={})
    @patch("services.entitlements.get_active_subscription")
    def test_active_subscription_is_exposed_without_payment_details(self, active, usage):
        subscription = SimpleNamespace(
            id=11,
            status="ACTIVE",
            current_period_start=NOW,
            current_period_end=datetime(2026, 11, 22, 16, 30, tzinfo=timezone.utc),
        )
        plan = SimpleNamespace(
            code="STUDENT_PRO",
            name="학생 Pro 30일 이용권",
            features={"AI_EXPLANATION": {"daily_limit": 50}},
        )
        active.return_value = (subscription, plan)
        snapshot = get_entitlement_snapshot(
            MagicMock(), SimpleNamespace(id=7, role=UserRole.STUDENT), NOW
        )
        self.assertEqual(snapshot["plan_code"], "STUDENT_PRO")
        self.assertEqual(snapshot["subscription"]["id"], 11)
        self.assertNotIn("payment_key", snapshot["subscription"])


if __name__ == "__main__":
    unittest.main()
