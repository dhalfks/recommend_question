from datetime import datetime, timezone
from pathlib import Path
import unittest
from unittest.mock import MagicMock

from services.subscriptions import expire_due_subscriptions


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


if __name__ == "__main__":
    unittest.main()
