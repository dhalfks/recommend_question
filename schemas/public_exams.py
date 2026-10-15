from datetime import date, datetime
from uuid import UUID
from typing import Literal, Optional

from pydantic import BaseModel, ConfigDict, Field, model_validator


QuestionType = Literal["MULTIPLE_CHOICE", "SHORT_ANSWER"]
AnswerVerificationStatus = Literal["MISSING", "UNVERIFIED", "VERIFIED"]
PublicationStatus = Literal["DRAFT", "READY", "PUBLISHED", "ARCHIVED"]


class OrmResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class PublicExamCreate(BaseModel):
    code: str = Field(min_length=1, max_length=64)
    name: str = Field(min_length=1, max_length=200)
    description: Optional[str] = None
    is_active: bool = True


class PublicExamUpdate(BaseModel):
    code: Optional[str] = Field(default=None, min_length=1, max_length=64)
    name: Optional[str] = Field(default=None, min_length=1, max_length=200)
    description: Optional[str] = None
    is_active: Optional[bool] = None


class PublicExamResponse(OrmResponse):
    id: int
    code: str
    name: str
    description: Optional[str]
    is_active: bool
    created_at: datetime
    updated_at: datetime


class PublicExamRoundCreate(BaseModel):
    exam_year: int = Field(ge=1900, le=2200)
    round_identifier: str = Field(min_length=1, max_length=100)
    display_name: Optional[str] = Field(default=None, max_length=255)
    held_on: Optional[date] = None
    is_published: bool = False


class PublicExamRoundUpdate(BaseModel):
    exam_year: Optional[int] = Field(default=None, ge=1900, le=2200)
    round_identifier: Optional[str] = Field(default=None, min_length=1, max_length=100)
    display_name: Optional[str] = Field(default=None, max_length=255)
    held_on: Optional[date] = None
    is_published: Optional[bool] = None


class PublicExamRoundResponse(OrmResponse):
    id: int
    exam_id: int
    exam_year: int
    round_identifier: str
    display_name: Optional[str]
    held_on: Optional[date]
    is_published: bool
    created_at: datetime
    updated_at: datetime


class PublicExamSubjectCreate(BaseModel):
    code: Optional[str] = Field(default=None, max_length=64)
    name: str = Field(min_length=1, max_length=200)
    display_order: int = Field(gt=0)


class PublicExamSubjectUpdate(BaseModel):
    code: Optional[str] = Field(default=None, max_length=64)
    name: Optional[str] = Field(default=None, min_length=1, max_length=200)
    display_order: Optional[int] = Field(default=None, gt=0)


class PublicExamSubjectResponse(OrmResponse):
    id: int
    round_id: int
    code: Optional[str]
    name: str
    display_order: int
    created_at: datetime
    updated_at: datetime


class PublicExamQuestionCreate(BaseModel):
    source_document_id: Optional[int] = None
    question_number: int = Field(gt=0)
    content: str = Field(min_length=1)
    options: Optional[list[str]] = None
    question_type: QuestionType = "MULTIPLE_CHOICE"
    correct_option: Optional[int] = Field(default=None, gt=0)
    correct_answer: Optional[str] = None
    explanation: Optional[str] = None
    source_page: Optional[int] = Field(default=None, gt=0)
    answer_verification_status: AnswerVerificationStatus = "MISSING"
    publication_status: PublicationStatus = "DRAFT"
    review_notes: Optional[str] = None

    @model_validator(mode="after")
    def validate_answer_state(self):
        if not self.content.strip():
            raise ValueError("문제 본문은 비어 있을 수 없습니다.")
        if self.question_type == "MULTIPLE_CHOICE":
            if not self.options or len(self.options) < 2:
                raise ValueError("객관식 문항에는 보기가 2개 이상 필요합니다.")
            if self.correct_answer is not None:
                raise ValueError("객관식 문항은 correct_answer를 사용할 수 없습니다.")
            if self.correct_option is not None and self.correct_option > len(self.options):
                raise ValueError("정답 보기 번호가 보기 개수를 초과합니다.")
        else:
            if self.options is not None or self.correct_option is not None:
                raise ValueError("단답형 문항은 보기와 정답 보기 번호를 사용할 수 없습니다.")
        if self.answer_verification_status == "MISSING" and (
            self.correct_option is not None or self.correct_answer is not None
        ):
            raise ValueError("정답 미확인 문항에는 정답을 입력할 수 없습니다.")
        if self.answer_verification_status == "VERIFIED" and not (
            self.correct_option is not None
            or (self.correct_answer is not None and self.correct_answer.strip())
        ):
            raise ValueError("검수 완료 문항에는 확인된 정답이 필요합니다.")
        if self.publication_status == "PUBLISHED" and self.answer_verification_status != "VERIFIED":
            raise ValueError("검수 완료된 문항만 게시할 수 있습니다.")
        return self


class PublicExamQuestionUpdate(BaseModel):
    source_document_id: Optional[int] = None
    question_number: Optional[int] = Field(default=None, gt=0)
    content: Optional[str] = Field(default=None, min_length=1)
    options: Optional[list[str]] = None
    question_type: Optional[QuestionType] = None
    correct_option: Optional[int] = Field(default=None, gt=0)
    correct_answer: Optional[str] = None
    explanation: Optional[str] = None
    source_page: Optional[int] = Field(default=None, gt=0)
    answer_verification_status: Optional[AnswerVerificationStatus] = None
    publication_status: Optional[PublicationStatus] = None
    review_notes: Optional[str] = None


class PublicExamQuestionStudentResponse(OrmResponse):
    id: int
    subject_id: int
    question_number: int
    content: str
    options: Optional[list[str]]
    question_type: QuestionType


class PublicExamQuestionAdminResponse(PublicExamQuestionStudentResponse):
    source_document_id: Optional[int]
    correct_option: Optional[int]
    correct_answer: Optional[str]
    explanation: Optional[str]
    source_page: Optional[int]
    answer_verification_status: AnswerVerificationStatus
    publication_status: PublicationStatus
    review_notes: Optional[str]
    created_at: datetime
    updated_at: datetime


class PublicExamSourceDocumentResponse(OrmResponse):
    id: int
    round_id: int
    original_file_name: str
    source_url: Optional[str]
    source_organization: Optional[str]
    source_notes: Optional[str]
    sha256: Optional[str]
    uploaded_by: int
    uploaded_at: datetime
    question_count: int = 0
    verified_count: int = 0
    published_count: int = 0


class PublicExamSourceDocumentDetail(PublicExamSourceDocumentResponse):
    questions: list[PublicExamQuestionAdminResponse]


class PublicExamDocumentUploadResponse(PublicExamSourceDocumentDetail):
    extraction_message: str


class PublicExamDocumentPublishResponse(BaseModel):
    document_id: int
    published_count: int


class PublicExamAnswerSave(BaseModel):
    selected_option: Optional[int] = Field(default=None, gt=0)
    written_answer: Optional[str] = None
    elapsed_seconds: float = Field(ge=0)

    @model_validator(mode="after")
    def validate_single_answer_kind(self):
        if self.selected_option is not None and self.written_answer is not None:
            raise ValueError("객관식과 단답형 답안을 동시에 저장할 수 없습니다.")
        return self


class PublicExamAttemptAnswerProgress(BaseModel):
    question: PublicExamQuestionStudentResponse
    sequence_number: int
    selected_option: Optional[int]
    written_answer: Optional[str]
    elapsed_seconds: float
    answered_at: Optional[datetime]


class PublicExamAttemptProgress(BaseModel):
    id: UUID
    subject_id: int
    status: Literal["IN_PROGRESS", "SUBMITTED", "ABANDONED"]
    started_at: datetime
    last_activity_at: datetime
    total_questions: int
    answers: list[PublicExamAttemptAnswerProgress]


class PublicExamAttemptResultItem(BaseModel):
    question_id: int
    sequence_number: int
    question_number: int
    content: str
    options: Optional[list[str]]
    question_type: QuestionType
    selected_option: Optional[int]
    written_answer: Optional[str]
    correct_option: Optional[int]
    correct_answer: Optional[str]
    explanation: Optional[str]
    elapsed_seconds: float
    is_correct: bool


class PublicExamAttemptResult(BaseModel):
    attempt_id: UUID
    exam_name: str
    exam_year: int
    round_identifier: str
    subject_name: str
    status: Literal["SUBMITTED"]
    started_at: datetime
    submitted_at: datetime
    total_elapsed_seconds: int
    total_questions: int
    correct_answers: int
    incorrect_answers: int
    score_percent: float
    items: list[PublicExamAttemptResultItem]


class PublicExamWrongAnswers(BaseModel):
    attempt_id: UUID
    items: list[PublicExamAttemptResultItem]
