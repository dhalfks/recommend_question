from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
MIGRATION = (ROOT / "migrations/20261023_add_billing_tables.sql").read_text(
    encoding="utf-8"
)
ROLLBACK = (
    ROOT / "migrations/20261023_add_billing_tables_rollback.sql"
).read_text(encoding="utf-8")


class BillingMigrationContractTests(unittest.TestCase):
    def test_migration_only_creates_expected_billing_tables(self):
        expected = {
            "billing_plans",
            "user_subscriptions",
            "payment_orders",
            "payment_transactions",
            "ai_usage_events",
            "payment_webhook_events",
        }
        for table in expected:
            self.assertIn(f"CREATE TABLE {table}", MIGRATION)

        self.assertNotIn("ALTER TABLE users", MIGRATION)
        self.assertNotIn("ALTER TABLE questions", MIGRATION)
        self.assertNotIn("DROP TABLE users", MIGRATION)
        self.assertNotIn("DROP TABLE questions", MIGRATION)

    def test_user_foreign_keys_match_production_integer_key(self):
        self.assertGreaterEqual(
            MIGRATION.count("user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE RESTRICT"),
            3,
        )

    def test_payment_idempotency_constraints_exist(self):
        self.assertIn("UNIQUE (order_id)", MIGRATION)
        self.assertIn("UNIQUE (idempotency_key)", MIGRATION)
        self.assertIn("UNIQUE (provider, event_id)", MIGRATION)
        self.assertIn("uq_payment_transactions_provider_payment_success", MIGRATION)

    def test_amounts_and_periods_are_validated(self):
        self.assertIn("billing_plans_price_positive CHECK (price > 0)", MIGRATION)
        self.assertIn("payment_orders_amount_positive CHECK (amount > 0)", MIGRATION)
        self.assertIn("current_period_end > current_period_start", MIGRATION)

    def test_initial_plans_are_server_owned_seed_data(self):
        self.assertIn("'STUDENT_PRO'", MIGRATION)
        self.assertIn("'TEACHER_PRO'", MIGRATION)
        self.assertIn("4900", MIGRATION)
        self.assertIn("49000", MIGRATION)
        self.assertIn("'ONE_TIME'", MIGRATION)

    def test_rollback_drops_only_new_tables_in_dependency_order(self):
        expected_order = [
            "payment_webhook_events",
            "ai_usage_events",
            "payment_transactions",
            "payment_orders",
            "user_subscriptions",
            "billing_plans",
        ]
        positions = [ROLLBACK.index(f"DROP TABLE {table}") for table in expected_order]
        self.assertEqual(positions, sorted(positions))
        self.assertNotIn("DROP TABLE users", ROLLBACK)
        self.assertNotIn("DROP TABLE questions", ROLLBACK)


if __name__ == "__main__":
    unittest.main()
