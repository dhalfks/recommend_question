from pathlib import Path
import unittest
from unittest.mock import MagicMock, patch

from services.payment_webhooks import _event_id, _safe_payload
from services.toss_payments import TossPaymentError, TossPaymentsClient


ROOT = Path(__file__).resolve().parents[1]


class TossWebhookTests(unittest.TestCase):
    def test_transmission_id_is_preferred_for_deduplication(self):
        self.assertEqual(_event_id("delivery-123", {"orderId": "order-1"}), "delivery-123")

    def test_fallback_event_id_is_stable(self):
        first = _event_id(None, {"status": "DONE", "orderId": "order-1"})
        second = _event_id(None, {"orderId": "order-1", "status": "DONE"})
        self.assertEqual(first, second)
        self.assertTrue(first.startswith("derived:"))

    def test_stored_payload_excludes_payment_personal_data(self):
        safe = _safe_payload({
            "orderId": "order-1", "status": "DONE", "paymentKey": "key",
            "card": {"number": "1234"}, "customerEmail": "private@example.com",
        })
        self.assertEqual(safe["orderId"], "order-1")
        self.assertNotIn("card", safe)
        self.assertNotIn("customerEmail", safe)

    @patch("services.toss_payments.httpx.get")
    def test_payment_query_uses_secret_authorization(self, get):
        response = MagicMock()
        response.is_error = False
        response.json.return_value = {"orderId": "order-1", "status": "DONE"}
        get.return_value = response
        client = TossPaymentsClient("test_gsk_secret", "https://api.tosspayments.com")
        result = client.get_payment_by_order_id(order_id="order-1")
        self.assertEqual(result["status"], "DONE")
        kwargs = get.call_args.kwargs
        self.assertTrue(kwargs["headers"]["Authorization"].startswith("Basic "))

    @patch("services.toss_payments.httpx.get", side_effect=Exception("unexpected"))
    def test_contract_documents_webhook_route_and_requery(self, _):
        route = (ROOT / "routes/billing.py").read_text(encoding="utf-8")
        service = (ROOT / "services/payment_webhooks.py").read_text(encoding="utf-8")
        self.assertIn('@router.post("/webhooks/toss"', route)
        self.assertIn("get_payment_by_order_id", service)
        self.assertIn('webhook_status == "DONE"', service)
        self.assertIn("reconcile_paid_payment", service)
        self.assertIn('existing.status == "PROCESSED"', service)


if __name__ == "__main__":
    unittest.main()
