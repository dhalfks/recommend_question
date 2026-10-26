from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]


class AIUsageAnalyticsContractTests(unittest.TestCase):
    def test_admin_api_is_role_protected_and_period_limited(self):
        route = (ROOT / "routes/billing.py").read_text(encoding="utf-8")
        self.assertIn('@router.get("/admin/ai-usage"', route)
        self.assertIn("days: int = Query(default=30, ge=1, le=90)", route)
        self.assertIn("Depends(require_roles(UserRole.ADMIN))", route)

    def test_analytics_groups_features_and_users_without_personal_ai_content(self):
        service = (ROOT / "services/ai_usage_analytics.py").read_text(encoding="utf-8")
        self.assertIn("group_by(AIUsageEvent.feature_code)", service)
        self.assertIn("group_by(User.id, User.name, User.email)", service)
        self.assertIn(".limit(20)", service)
        self.assertNotIn("prompt", service.lower())
        self.assertNotIn("response_text", service)

    def test_cost_is_explicitly_configurable(self):
        config = (ROOT / "config.py").read_text(encoding="utf-8")
        service = (ROOT / "services/ai_usage_analytics.py").read_text(encoding="utf-8")
        self.assertIn("AI_INPUT_COST_PER_MILLION_KRW", config)
        self.assertIn("AI_OUTPUT_COST_PER_MILLION_KRW", config)
        self.assertIn('"cost_configured"', service)

    def test_admin_frontend_exposes_usage_dashboard(self):
        page = (ROOT / "frontend/src/pages/admin/ai-usage.tsx").read_text(encoding="utf-8")
        nav = (ROOT / "frontend/src/components/Navbar.tsx").read_text(encoding="utf-8")
        self.assertIn("roles={['ADMIN']}", page)
        self.assertIn("billingAPI.adminAIUsage", page)
        self.assertIn("AI 사용 분석", page)
        self.assertIn('href="/admin/ai-usage"', nav)


if __name__ == "__main__":
    unittest.main()
