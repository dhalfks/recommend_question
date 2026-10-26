from pathlib import Path
import json
import unittest


ROOT = Path(__file__).resolve().parents[1]


class BillingReleaseReadinessTests(unittest.TestCase):
    def test_public_api_health_route_exists(self):
        main = (ROOT / "main.py").read_text(encoding="utf-8")
        self.assertIn('@app.get("/api/health")', main)

    def test_daily_subscription_expiry_cron_targets_api(self):
        config = json.loads((ROOT / "vercel.json").read_text(encoding="utf-8"))
        self.assertIn(
            {
                "path": "/api/billing/cron/subscriptions/expire",
                "schedule": "10 15 * * *",
            },
            config["crons"],
        )

    def test_release_checklist_covers_required_production_settings(self):
        checklist = (ROOT / "docs/BILLING_RELEASE_CHECKLIST.md").read_text(encoding="utf-8")
        for variable in (
            "NEXT_PUBLIC_API_URL",
            "DATABASE_URL",
            "JWT_SECRET_KEY",
            "TOSS_SECRET_KEY",
            "NEXT_PUBLIC_TOSS_CLIENT_KEY",
            "CRON_SECRET",
        ):
            self.assertIn(variable, checklist)


if __name__ == "__main__":
    unittest.main()
