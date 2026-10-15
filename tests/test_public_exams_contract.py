import unittest
from datetime import datetime, timedelta, timezone
from decimal import Decimal
from types import SimpleNamespace
from uuid import uuid4

from fastapi import HTTPException
from pydantic import ValidationError

from models import PublicExamAttempt, PublicExamAttemptAnswer, PublicExamQuestion, UserRole
from routes.public_exams import admin_only, router, student_only
from routes.public_exams import (
    _grade_public_exam_answer,
    _owned_attempt_query,
    _public_question_query,
    _require_in_progress,
    _server_elapsed_seconds,
)
from sqlalchemy.dialects import postgresql
from sqlalchemy.orm import Session
from schemas.public_exams import (
    PublicExamQuestionCreate,
    PublicExamQuestionStudentResponse,
)


class PublicExamContractTests(unittest.TestCase):
    def test_student_response_does_not_serialize_answer_fields(self):
        source = SimpleNamespace(
            id=1,
            subject_id=2,
            question_number=3,
            content="공개 문제",
            options=["보기 1", "보기 2"],
            question_type="MULTIPLE_CHOICE",
            correct_option=1,
            correct_answer=None,
            explanation="노출되면 안 되는 해설",
            answer_verification_status="VERIFIED",
            review_notes="관리자 메모",
        )

        payload = PublicExamQuestionStudentResponse.model_validate(source).model_dump()

        self.assertEqual(
            set(payload),
            {
                "id",
                "subject_id",
                "question_number",
                "content",
                "options",
                "question_type",
            },
        )
        self.assertNotIn("correct_option", payload)
        self.assertNotIn("correct_answer", payload)
        self.assertNotIn("explanation", payload)
        self.assertNotIn("answer_verification_status", payload)
        self.assertNotIn("review_notes", payload)

    def test_unverified_question_cannot_be_published(self):
        with self.assertRaises(ValidationError):
            PublicExamQuestionCreate(
                question_number=1,
                content="문제",
                options=["1", "2"],
                question_type="MULTIPLE_CHOICE",
                correct_option=1,
                answer_verification_status="UNVERIFIED",
                publication_status="PUBLISHED",
            )

    def test_missing_answer_cannot_contain_guessed_answer(self):
        with self.assertRaises(ValidationError):
            PublicExamQuestionCreate(
                question_number=1,
                content="문제",
                options=["1", "2"],
                question_type="MULTIPLE_CHOICE",
                correct_option=1,
                answer_verification_status="MISSING",
            )

    def test_admin_dependency_rejects_student(self):
        with self.assertRaises(HTTPException) as context:
            admin_only(SimpleNamespace(role=UserRole.STUDENT))
        self.assertEqual(context.exception.status_code, 403)

    def test_admin_dependency_accepts_admin(self):
        admin = SimpleNamespace(role=UserRole.ADMIN)
        self.assertIs(admin_only(admin), admin)

    def test_public_query_requires_published_verified_content(self):
        query = _public_question_query(Session())
        compiled = query.statement.compile(dialect=postgresql.dialect())
        values = set(compiled.params.values())
        sql = str(compiled)

        self.assertIn("public_exams.is_active IS true", sql)
        self.assertIn("public_exam_rounds.is_published IS true", sql)
        self.assertIn("PUBLISHED", values)
        self.assertIn("VERIFIED", values)

    def test_every_content_mutation_and_admin_read_uses_admin_dependency(self):
        protected_routes = [
            route
            for route in router.routes
            if route.path.startswith("/admin/")
            or (
                {"POST", "PUT"} & route.methods
                and "attempt" not in route.endpoint.__name__
                and "answer" not in route.endpoint.__name__
            )
        ]
        self.assertTrue(protected_routes)
        for route in protected_routes:
            calls = {dependency.call for dependency in route.dependant.dependencies}
            self.assertIn(admin_only, calls, route.path)

    def test_attempt_routes_use_student_dependency(self):
        attempt_routes = [
            route
            for route in router.routes
            if "attempt" in route.endpoint.__name__ or route.endpoint.__name__ == "save_public_exam_answer"
        ]
        self.assertTrue(attempt_routes)
        for route in attempt_routes:
            calls = {dependency.call for dependency in route.dependant.dependencies}
            self.assertIn(student_only, calls, route.path)

    def test_owned_attempt_query_contains_user_and_attempt_filters(self):
        attempt_id = uuid4()
        query = _owned_attempt_query(Session(), attempt_id, 42)
        compiled = query.statement.compile(dialect=postgresql.dialect())

        self.assertIn("public_exam_attempts.id", str(compiled))
        self.assertIn("public_exam_attempts.user_id", str(compiled))
        self.assertIn(attempt_id, compiled.params.values())
        self.assertIn(42, compiled.params.values())

    def test_duplicate_submission_is_rejected(self):
        with self.assertRaises(HTTPException) as context:
            _require_in_progress(SimpleNamespace(status="SUBMITTED"))
        self.assertEqual(context.exception.status_code, 409)

    def test_multiple_choice_grading(self):
        question = PublicExamQuestion(
            question_type="MULTIPLE_CHOICE",
            correct_option=2,
            answer_verification_status="VERIFIED",
        )
        correct = PublicExamAttemptAnswer(selected_option=2)
        wrong = PublicExamAttemptAnswer(selected_option=1)

        self.assertTrue(_grade_public_exam_answer(question, correct))
        self.assertFalse(_grade_public_exam_answer(question, wrong))

    def test_unanswered_question_is_graded_incorrect(self):
        question = PublicExamQuestion(
            question_type="MULTIPLE_CHOICE",
            correct_option=1,
            answer_verification_status="VERIFIED",
        )
        unanswered = PublicExamAttemptAnswer(selected_option=None, written_answer=None)

        self.assertFalse(_grade_public_exam_answer(question, unanswered))

    def test_unverified_question_cannot_be_graded(self):
        question = PublicExamQuestion(
            question_type="MULTIPLE_CHOICE",
            correct_option=1,
            answer_verification_status="UNVERIFIED",
        )

        with self.assertRaises(HTTPException) as context:
            _grade_public_exam_answer(question, PublicExamAttemptAnswer(selected_option=1))
        self.assertEqual(context.exception.status_code, 409)

    def test_short_answer_grading_normalizes_whitespace_and_newlines(self):
        question = PublicExamQuestion(
            question_type="SHORT_ANSWER",
            correct_answer="SELECT 1;\n",
            answer_verification_status="VERIFIED",
        )
        answer = PublicExamAttemptAnswer(written_answer=" SELECT 1;\r\n")

        self.assertTrue(_grade_public_exam_answer(question, answer))

    def test_server_elapsed_time_uses_timestamps(self):
        started = datetime(2026, 10, 15, 1, 0, tzinfo=timezone.utc)
        submitted = started + timedelta(hours=1, minutes=2, seconds=3, milliseconds=900)

        self.assertEqual(_server_elapsed_seconds(started, submitted), 3723)

    def test_progress_schema_preserves_answer_and_item_elapsed_time(self):
        from schemas.public_exams import PublicExamAttemptProgress

        payload = PublicExamAttemptProgress.model_validate(
            {
                "id": uuid4(),
                "subject_id": 10,
                "status": "IN_PROGRESS",
                "started_at": datetime.now(timezone.utc),
                "last_activity_at": datetime.now(timezone.utc),
                "total_questions": 1,
                "answers": [
                    {
                        "question": {
                            "id": 20,
                            "subject_id": 10,
                            "question_number": 1,
                            "content": "문제",
                            "options": ["1", "2"],
                            "question_type": "MULTIPLE_CHOICE",
                        },
                        "sequence_number": 1,
                        "selected_option": 2,
                        "written_answer": None,
                        "elapsed_seconds": Decimal("12.5"),
                        "answered_at": datetime.now(timezone.utc),
                    }
                ],
            }
        )

        self.assertEqual(payload.answers[0].selected_option, 2)
        self.assertEqual(payload.answers[0].elapsed_seconds, 12.5)
        serialized_question = payload.model_dump()["answers"][0]["question"]
        self.assertNotIn("correct_option", serialized_question)
        self.assertNotIn("correct_answer", serialized_question)
        self.assertNotIn("explanation", serialized_question)


if __name__ == "__main__":
    unittest.main()
