from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]


def read(relative_path: str) -> str:
    return (ROOT / relative_path).read_text(encoding="utf-8")


class RefundRequestContractTests(unittest.TestCase):
    def test_migration_preserves_audit_and_prevents_duplicate_pending(self):
        sql = read("migrations/20261023_add_refund_requests.sql")
        self.assertIn("CREATE TABLE refund_requests", sql)
        self.assertIn("eligibility_snapshot JSONB NOT NULL", sql)
        self.assertIn("refund_transaction_id BIGINT", sql)
        self.assertIn("uq_refund_requests_pending_order", sql)
        self.assertIn("WHERE status = 'PENDING'", sql)
        self.assertIn("REFERENCES payment_orders(id) ON DELETE RESTRICT", sql)

    def test_service_scopes_order_and_reuses_secure_refund(self):
        source = read("services/refund_requests.py")
        self.assertIn("PaymentOrder.user_id == user.id", source)
        self.assertIn('order.status != "PAID"', source)
        self.assertIn("evaluate_refund_policy(db, order)", source)
        self.assertIn("refund_payment(", source)
        self.assertIn('request.status = "APPROVED"', source)
        self.assertIn('request.status = "REJECTED"', source)

    def test_routes_require_admin_for_decisions(self):
        source = read("routes/billing.py")
        self.assertIn('@router.post("/refund-requests"', source)
        self.assertIn('@router.get("/refund-requests"', source)
        self.assertIn('@router.get("/admin/refund-requests"', source)
        self.assertIn('@router.post("/admin/refund-requests/{request_id}/approve"', source)
        self.assertIn('@router.post("/admin/refund-requests/{request_id}/reject"', source)
        self.assertGreaterEqual(source.count("Depends(require_roles(UserRole.ADMIN))"), 6)

    def test_frontend_exposes_user_request_and_admin_decisions(self):
        api = read("frontend/src/lib/api.ts")
        profile = read("frontend/src/components/BillingSummary.tsx")
        admin = read("frontend/src/pages/admin/billing.tsx")
        self.assertIn("requestRefund", api)
        self.assertIn("approveRefundRequest", api)
        self.assertIn("rejectRefundRequest", api)
        self.assertIn("환불 신청", profile)
        self.assertIn("Promise.allSettled", profile)
        self.assertIn("환불 신청 관리", admin)
        self.assertIn(">승인</button>", admin)
        self.assertIn(">반려</button>", admin)


if __name__ == "__main__":
    unittest.main()
