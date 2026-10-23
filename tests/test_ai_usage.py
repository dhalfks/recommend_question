from pathlib import Path
from types import SimpleNamespace
import unittest
from unittest.mock import MagicMock, patch

from models import AIUsageEvent, UserRole
from services.ai_usage import complete_ai_usage, reserve_ai_usage


ROOT = Path(__file__).resolve().parents[1]
FILES_ROUTE = (ROOT / "routes/files.py").read_text(encoding="utf-8")
PROGRESS_ROUTE = (ROOT / "routes/progress.py").read_text(encoding="utf-8")
QUESTIONS_ROUTE = (ROOT / "routes/questions.py").read_text(encoding="utf-8")


class AIUsageReservationTests(unittest.TestCase):
    @patch("services.ai_usage.get_active_subscription", return_value=None)
    @patch("services.ai_usage.ensure_feature_available")
    def test_reservation_locks_user_before_check_and_commits_started_event(
        self, ensure, active
    ):
        db = MagicMock()
        user = SimpleNamespace(id=7, role=UserRole.STUDENT)
        added = []
        db.add.side_effect = added.append

        event = reserve_ai_usage(db, user, "CODE_REVIEW", "request-1")

        db.execute.assert_called_once()
        ensure.assert_called_once_with(db, user, "CODE_REVIEW")
        self.assertEqual(event.status, "STARTED")
        self.assertEqual(event.request_id, "request-1")
        self.assertIsNone(event.subscription_id)
        self.assertIs(added[0], event)
        db.commit.assert_called_once()

    @patch("services.ai_usage.get_active_subscription")
    @patch("services.ai_usage.ensure_feature_available")
    def test_paid_reservation_records_subscription(self, ensure, active):
        active.return_value = (SimpleNamespace(id=44), SimpleNamespace())
        db = MagicMock()
        user = SimpleNamespace(id=7, role=UserRole.STUDENT)

        event = reserve_ai_usage(db, user, "AI_EXPLANATION", "request-2")

        self.assertEqual(event.subscription_id, 44)

    def test_completion_records_tokens_and_failure_state(self):
        db = MagicMock()
        event = AIUsageEvent(status="STARTED")

        complete_ai_usage(
            db,
            event,
            succeeded=False,
            usage={"input_tokens": "12", "output_tokens": 5},
            failure_code="MODEL_ERROR",
        )

        self.assertEqual(event.status, "FAILED")
        self.assertEqual(event.input_tokens, 12)
        self.assertEqual(event.output_tokens, 5)
        self.assertEqual(event.failure_code, "MODEL_ERROR")
        self.assertIsNotNone(event.completed_at)
        db.commit.assert_called_once()


class AIUsageIntegrationContractTests(unittest.TestCase):
    def test_question_generation_is_reserved_and_completed(self):
        self.assertIn(
            'reserve_ai_usage(db, current_user, "QUESTION_GENERATION")',
            FILES_ROUTE,
        )
        self.assertIn("complete_ai_usage(", FILES_ROUTE)

    def test_code_review_uses_tracked_wrapper(self):
        self.assertIn(
            'reserve_ai_usage(usage_db, current_user, "CODE_REVIEW")',
            PROGRESS_ROUTE,
        )
        self.assertIn("usage_db = SessionLocal()", PROGRESS_ROUTE)
        self.assertIn("usage_db.close()", PROGRESS_ROUTE)
        self.assertIn("await tracked_code_review", PROGRESS_ROUTE)

    def test_answer_enrichment_is_preflighted(self):
        self.assertIn(
            'ensure_feature_available(db, current_user, "QUESTION_GENERATION")',
            QUESTIONS_ROUTE,
        )
        self.assertIn("current_user.id", QUESTIONS_ROUTE)


if __name__ == "__main__":
    unittest.main()
