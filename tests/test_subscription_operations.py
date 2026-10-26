from datetime import datetime, timezone
from pathlib import Path
import unittest
from unittest.mock import MagicMock, patch

from fastapi import HTTPException

from services.subscriptions import expire_due_subscriptions
from routes.billing import verify_cron_authorization


ROOT = Path(__file__).resolve().parents[1]


class SubscriptionOperationsTests(unittest.TestCase):
    def test_expiry_updates_only_due_active_subscriptions(self):
        db = MagicMock()
        query = db.query.return_value
        query.filter.return_value.update.return_value = 3
        now = datetime(2026, 10, 26, tzinfo=timezone.utc)
        count = expire_due_subscriptions(db, now=now)
        self.assertEqual(count, 3)
        query.filter.return_value.update.assert_called_once()
        db.commit.assert_called_once()

    def test_admin_routes_are_protected(self):
        route = (ROOT / "routes/billing.py").read_text(encoding="utf-8")
        self.assertIn('@router.get("/admin/subscriptions"', route)
        self.assertIn('@router.post("/admin/subscriptions/expire"', route)
        self.assertIn("list_admin_subscriptions", route)
        self.assertIn("expire_due_subscriptions", route)

    def test_admin_page_exposes_expiry_reconciliation(self):
        page = (ROOT / "frontend/src/pages/admin/subscriptions.tsx").read_text(encoding="utf-8")
        nav = (ROOT / "frontend/src/components/Navbar.tsx").read_text(encoding="utf-8")
        self.assertIn("roles={['ADMIN']}", page)
        self.assertIn("만료 상태 정리", page)
        self.assertIn("billingAPI.expireSubscriptions", page)
        self.assertIn('href="/admin/subscriptions"', nav)

    def test_cron_authorization_accepts_only_configured_bearer_secret(self):
        with patch("routes.billing.settings.CRON_SECRET", "a-secure-cron-secret"):
            verify_cron_authorization("Bearer a-secure-cron-secret")
            with self.assertRaises(HTTPException) as invalid:
                verify_cron_authorization("Bearer wrong-secret")
            self.assertEqual(invalid.exception.status_code, 401)

    def test_cron_authorization_fails_closed_without_secret(self):
        with patch("routes.billing.settings.CRON_SECRET", ""):
            with self.assertRaises(HTTPException) as missing:
                verify_cron_authorization(None)
            self.assertEqual(missing.exception.status_code, 503)

    def test_vercel_runs_daily_expiry_cron(self):
        config = (ROOT / "vercel.json").read_text(encoding="utf-8")
        route = (ROOT / "routes/billing.py").read_text(encoding="utf-8")
        self.assertIn('"path": "/api/billing/cron/subscriptions/expire"', config)
        self.assertIn('"schedule": "10 15 * * *"', config)
        self.assertIn('@router.get("/cron/subscriptions/expire"', route)
        self.assertIn("verify_cron_authorization(authorization)", route)


if __name__ == "__main__":
    unittest.main()
