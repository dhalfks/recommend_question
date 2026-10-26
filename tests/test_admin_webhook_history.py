from pathlib import Path
import unittest
from datetime import datetime, timezone
from types import SimpleNamespace
from unittest.mock import MagicMock

from services.payment_webhooks import list_admin_webhook_events


ROOT = Path(__file__).resolve().parents[1]


class AdminWebhookHistoryTests(unittest.TestCase):
    def test_service_returns_only_safe_operational_fields(self):
        event = SimpleNamespace(
            id=7, provider="TOSS", event_id="delivery-7",
            event_type="PAYMENT_STATUS_CHANGED", status="FAILED",
            payload={"orderId": "order-7", "status": "DONE", "paymentKey": "secret"},
            error_message="verification failed",
            received_at=datetime.now(timezone.utc), processed_at=None,
        )
        db = MagicMock()
        db.query.return_value.order_by.return_value.limit.return_value.all.return_value = [event]

        result = list_admin_webhook_events(db)

        self.assertEqual(result[0]["order_id"], "order-7")
        self.assertEqual(result[0]["payment_status"], "DONE")
        self.assertNotIn("payload", result[0])
        self.assertNotIn("paymentKey", result[0])

    def test_admin_webhook_endpoint_is_protected_and_filterable(self):
        route = (ROOT / "routes/billing.py").read_text(encoding="utf-8")
        self.assertIn('@router.get("/admin/webhooks"', route)
        self.assertIn("require_roles(UserRole.ADMIN)", route)
        self.assertIn("event_status=event_status", route)

    def test_webhook_history_does_not_expose_full_payload(self):
        service = (ROOT / "services/payment_webhooks.py").read_text(encoding="utf-8")
        self.assertIn('"order_id": (event.payload or {}).get("orderId")', service)
        self.assertNotIn('"payload": event.payload', service)

    def test_admin_page_uses_webhook_history_api(self):
        page = (ROOT / "frontend/src/pages/admin/webhooks.tsx").read_text(encoding="utf-8")
        navbar = (ROOT / "frontend/src/components/Navbar.tsx").read_text(encoding="utf-8")
        self.assertIn("billingAPI.adminWebhooks", page)
        self.assertIn("처리 실패", page)
        self.assertIn('href="/admin/webhooks"', navbar)


if __name__ == "__main__":
    unittest.main()
