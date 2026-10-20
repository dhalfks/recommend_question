from pathlib import Path
from types import SimpleNamespace
import unittest
from unittest.mock import MagicMock

from fastapi import HTTPException
from pydantic import ValidationError

from routes.exam_papers import _paper_items
from schemas.exam_papers import ExamPaperWrite


ROOT = Path(__file__).resolve().parents[1]
ROUTE = (ROOT / "routes/exam_papers.py").read_text(encoding="utf-8")
MAIN = (ROOT / "main.py").read_text(encoding="utf-8")
MIGRATION = (ROOT / "migrations/20261020_exam_papers.sql").read_text(encoding="utf-8")
EDITOR = (ROOT / "frontend/src/components/ExamPaperEditor.tsx").read_text(encoding="utf-8")
PRINT_PAGE = (ROOT / "frontend/src/pages/exam-papers/[paperId]/print.tsx").read_text(encoding="utf-8")


class ExamPaperSchemaTests(unittest.TestCase):
    def test_write_contract_preserves_question_order(self):
        payload = ExamPaperWrite(title="  중간고사  ", question_ids=[9, 3, 7])
        self.assertEqual(payload.title, "중간고사")
        self.assertEqual(payload.question_ids, [9, 3, 7])

    def test_duplicate_questions_are_rejected(self):
        with self.assertRaises(ValidationError):
            ExamPaperWrite(title="중간고사", question_ids=[3, 3])

    def test_empty_paper_is_rejected(self):
        with self.assertRaises(ValidationError):
            ExamPaperWrite(title="중간고사", question_ids=[])


class ExamPaperSecurityContractTests(unittest.TestCase):
    def test_every_route_requires_professor_role(self):
        self.assertIn("professor_only = require_roles(UserRole.PROFESSOR)", ROUTE)
        self.assertEqual(ROUTE.count("Depends(professor_only)"), 5)

    def test_queries_and_selected_questions_are_scoped_to_owner(self):
        self.assertIn("ExamPaper.professor_id == professor_id", ROUTE)
        self.assertIn("Question.professor_id == professor_id", ROUTE)
        self.assertIn("본인이 소유하지 않거나 존재하지 않는 문항", ROUTE)

    def test_router_is_registered(self):
        self.assertIn('prefix="/api/exam-papers"', MAIN)

    def test_snapshot_builder_preserves_requested_order(self):
        first = SimpleNamespace(
            id=1, subject_id=10, title="첫 문제", content="내용 1",
            answer_type=SimpleNamespace(value="MULTIPLE_CHOICE"), options='["A", "B"]',
            code_snippet=None, correct_answer="0", correct_option=None, explanation="해설 1",
        )
        second = SimpleNamespace(
            id=2, subject_id=20, title="둘째 문제", content="내용 2",
            answer_type=SimpleNamespace(value="SUBJECTIVE"), options=None,
            code_snippet="SELECT 1", correct_answer="1", correct_option=None, explanation=None,
        )
        db = MagicMock()
        db.query.return_value.join.return_value.filter.return_value.all.return_value = [
            (first, "과목 A"), (second, "과목 B"),
        ]
        items = _paper_items(db, professor_id=7, question_ids=[2, 1])
        self.assertEqual([item.question_id for item in items], [2, 1])
        self.assertEqual([item.display_order for item in items], [1, 2])
        self.assertEqual(items[1].options, ["A", "B"])

    def test_snapshot_builder_rejects_inaccessible_question(self):
        db = MagicMock()
        db.query.return_value.join.return_value.filter.return_value.all.return_value = []
        with self.assertRaises(HTTPException) as raised:
            _paper_items(db, professor_id=7, question_ids=[99])
        self.assertEqual(raised.exception.status_code, 400)


class ExamPaperPersistenceContractTests(unittest.TestCase):
    def test_migration_enforces_order_and_question_uniqueness(self):
        self.assertIn("UNIQUE (exam_paper_id, display_order)", MIGRATION)
        self.assertIn("UNIQUE (exam_paper_id, question_id)", MIGRATION)
        self.assertIn("REFERENCES users(id) ON DELETE RESTRICT", MIGRATION)
        self.assertIn("REFERENCES exam_papers(id) ON DELETE CASCADE", MIGRATION)
        self.assertIn("trg_exam_papers_validate_professor", MIGRATION)

    def test_snapshot_fields_are_present(self):
        for field in ("subject_name", "title", "content", "options", "code_snippet", "correct_answer", "explanation"):
            self.assertIn(field, MIGRATION)


class ExamPaperFrontendContractTests(unittest.TestCase):
    def test_editor_has_drag_and_non_drag_controls(self):
        self.assertIn("draggable", EDITOR)
        self.assertIn("추가", EDITOR)
        self.assertIn("위로 이동", EDITOR)
        self.assertIn("아래로 이동", EDITOR)

    def test_frontend_pages_require_professor(self):
        self.assertIn("roles={['PROFESSOR']}", EDITOR)
        self.assertIn("roles={['PROFESSOR']}", PRINT_PAGE)

    def test_print_uses_browser_print_and_hides_answers_by_default(self):
        self.assertIn("useState(false)", PRINT_PAGE)
        self.assertIn("window.print()", PRINT_PAGE)
        self.assertIn("@media print", PRINT_PAGE)


if __name__ == "__main__":
    unittest.main()
