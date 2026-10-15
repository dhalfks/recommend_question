from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
ATTEMPT_PAGE = ROOT / "frontend/src/pages/public-exams/attempt/[attemptId].tsx"
RESULT_PAGE = ROOT / "frontend/src/pages/public-exams/results/[attemptId].tsx"


class PublicExamFrontendContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.attempt_source = ATTEMPT_PAGE.read_text(encoding="utf-8")
        cls.result_source = RESULT_PAGE.read_text(encoding="utf-8")

    def test_debounced_answers_are_tracked_for_unload_warning(self):
        self.assertIn("pendingDebouncesRef.current.add(questionId)", self.attempt_source)
        self.assertIn("pendingDebouncesRef.current.size > 0", self.attempt_source)
        self.assertIn("window.addEventListener('beforeunload', warnIfSaving)", self.attempt_source)

    def test_pending_debounces_are_flushed_through_the_save_queue(self):
        self.assertIn("pendingQuestionIds.map((questionId) => flushQuestionSave(questionId))", self.attempt_source)
        self.assertIn("saveQueuesRef.current[questionId] = next", self.attempt_source)
        self.assertIn("await Promise.allSettled(Object.values(saveQueuesRef.current))", self.attempt_source)

    def test_local_and_saved_versions_are_distinct(self):
        self.assertIn("localVersionsRef", self.attempt_source)
        self.assertIn("savedVersionsRef", self.attempt_source)
        self.assertIn("setSaveStates((current) => ({ ...current, [questionId]: 'error' }))", self.attempt_source)
        self.assertIn("retryCurrentSave", self.attempt_source)

    def test_wrong_answer_failure_is_isolated_from_primary_result(self):
        result_start = self.result_source.index("publicExamsAPI.getResult(attemptId)")
        result_set = self.result_source.index("setResult(resultResponse.data)", result_start)
        wrong_start = self.result_source.index("publicExamsAPI.getWrongAnswers(attemptId)", result_set)
        wrong_error = self.result_source.index("setWrongItemsError", wrong_start)
        self.assertLess(result_start, result_set)
        self.assertLess(result_set, wrong_start)
        self.assertLess(wrong_start, wrong_error)
        self.assertIn("disabled={!wrongItemsLoaded || !wrongItems.length}", self.result_source)


if __name__ == "__main__":
    unittest.main()
