from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
PRICING = (ROOT / "frontend/src/pages/pricing.tsx").read_text(encoding="utf-8")
CHECKOUT = (ROOT / "frontend/src/pages/billing/checkout.tsx").read_text(encoding="utf-8")
SUCCESS = (ROOT / "frontend/src/pages/billing/success.tsx").read_text(encoding="utf-8")
FAIL = (ROOT / "frontend/src/pages/billing/fail.tsx").read_text(encoding="utf-8")
API = (ROOT / "frontend/src/lib/api.ts").read_text(encoding="utf-8")
MIGRATION = (ROOT / "migrations/20261023_add_billing_customers.sql").read_text(
    encoding="utf-8"
)


class BillingFrontendContractTests(unittest.TestCase):
    def test_customer_key_is_random_and_stored_outside_users(self):
        self.assertIn("CREATE TABLE billing_customers", MIGRATION)
        self.assertIn("UNIQUE (user_id)", MIGRATION)
        self.assertIn("UNIQUE (customer_key)", MIGRATION)
        self.assertNotIn("ALTER TABLE users", MIGRATION)

    def test_pricing_creates_server_order_before_checkout(self):
        self.assertIn("billingAPI.createOrder(plan.code)", PRICING)
        self.assertIn("billing-order:${order.order_id}", PRICING)
        self.assertNotIn("amount:", PRICING.split("createOrder", 1)[1].split(";", 1)[0])

    def test_checkout_uses_toss_v2_widget_and_server_order_amount(self):
        self.assertIn("loadTossPayments", CHECKOUT)
        self.assertIn("widgets({ customerKey: order.customer_key! })", CHECKOUT)
        self.assertIn("value: order.amount", CHECKOUT)
        self.assertIn("renderPaymentMethods", CHECKOUT)
        self.assertIn("renderAgreement", CHECKOUT)
        self.assertIn("widgets.requestPayment", CHECKOUT)

    def test_checkout_cancels_widget_initialization_after_unmount(self):
        self.assertIn("window.requestAnimationFrame", CHECKOUT)
        self.assertIn("window.cancelAnimationFrame", CHECKOUT)
        self.assertIn("if (!active) return", CHECKOUT)
        self.assertIn("if (active) {", CHECKOUT)

    def test_success_calls_our_backend_not_toss_api(self):
        self.assertIn("billingAPI.confirm", SUCCESS)
        self.assertNotIn("api.tosspayments.com", SUCCESS)
        self.assertIn("payment_key: paymentKey", SUCCESS)

    def test_failure_does_not_confirm_payment(self):
        self.assertNotIn("billingAPI.confirm", FAIL)
        self.assertIn("PAY_PROCESS_CANCELED", FAIL)

    def test_api_has_all_billing_endpoints(self):
        for path in ("/billing/plans", "/billing/me", "/billing/orders", "/billing/payments/confirm"):
            self.assertIn(path, API)


if __name__ == "__main__":
    unittest.main()
