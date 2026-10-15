from pathlib import Path
import unittest

from services.public_exam_documents import extract_pdf_pages, parse_question_candidates


ROOT = Path(__file__).resolve().parents[1]
ROUTES = (ROOT / "routes/public_exams.py").read_text(encoding="utf-8")
SCHEMAS = (ROOT / "schemas/public_exams.py").read_text(encoding="utf-8")


class PublicExamDocumentContractTests(unittest.TestCase):
    def test_invalid_pdf_is_rejected(self):
        with self.assertRaisesRegex(ValueError, "PDF 파일을 읽을 수 없습니다"):
            extract_pdf_pages(b"not a pdf")

    def test_text_parser_extracts_questions_and_circled_options(self):
        questions = parse_question_candidates([
            "1. SQL의 설명으로 옳은 것은?\n① 보기 A\n② 보기 B\n"
            "2. 다음 용어를 쓰시오.\n설명 본문"
        ])
        self.assertEqual([item.question_number for item in questions], [1, 2])
        self.assertEqual(questions[0].options, ["보기 A", "보기 B"])
        self.assertIsNone(questions[1].options)

    def test_ambiguous_duplicate_numbers_are_not_imported(self):
        questions = parse_question_candidates(["1. 첫 문항\n1. 중복 문항"])
        self.assertEqual(questions, [])

    def test_upload_creates_only_draft_missing_questions(self):
        self.assertIn('answer_verification_status="MISSING"', ROUTES)
        self.assertIn('publication_status="DRAFT"', ROUTES)
        self.assertIn("정답은 자동 추측하지 않았습니다", ROUTES)

    def test_document_routes_require_admin(self):
        document_section = ROUTES[ROUTES.index('@router.get(\n    "/admin/documents"'):]
        for route in (
            "list_public_exam_documents_for_admin",
            "get_public_exam_document_for_admin",
            "download_public_exam_document_for_admin",
            "upload_public_exam_document_for_admin",
            "publish_public_exam_document_for_admin",
        ):
            start = document_section.index(f"def {route}")
            dependency = document_section.index("Depends(admin_only)", start)
            self.assertLess(dependency - start, 500)

    def test_publish_requires_verified_answers(self):
        self.assertIn('question.answer_verification_status != "VERIFIED"', ROUTES)
        self.assertIn('question.correct_option is None', ROUTES)
        self.assertIn('not _normalized_text(question.correct_answer)', ROUTES)
        self.assertIn('publication_status = "PUBLISHED"', ROUTES)

    def test_document_response_does_not_expose_storage_key(self):
        response_section = SCHEMAS[SCHEMAS.index("class PublicExamSourceDocumentResponse"):]
        response_section = response_section[:response_section.index("class PublicExamSourceDocumentDetail")]
        self.assertNotIn("storage_key", response_section)


if __name__ == "__main__":
    unittest.main()
