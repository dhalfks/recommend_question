from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator


AnswerType = Literal["MULTIPLE_CHOICE", "SUBJECTIVE", "CODE_INPUT"]


class ExamPaperWrite(BaseModel):
    title: str = Field(min_length=1, max_length=255)
    description: str | None = Field(default=None, max_length=2000)
    question_ids: list[int] = Field(min_length=1, max_length=200)

    @field_validator("title")
    @classmethod
    def normalize_title(cls, value: str) -> str:
        normalized = value.strip()
        if not normalized:
            raise ValueError("시험지 제목을 입력해 주세요.")
        return normalized

    @field_validator("question_ids")
    @classmethod
    def unique_questions(cls, value: list[int]) -> list[int]:
        if any(question_id <= 0 for question_id in value):
            raise ValueError("유효하지 않은 문항 ID가 포함되어 있습니다.")
        if len(value) != len(set(value)):
            raise ValueError("같은 문항을 시험지에 중복해서 넣을 수 없습니다.")
        return value


class ExamPaperItemResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    question_id: int
    display_order: int
    subject_id: int
    subject_name: str
    title: str
    content: str
    answer_type: AnswerType
    options: list[str] | None = None
    code_snippet: str | None = None
    correct_answer: str | None = None
    correct_option: int | None = None
    explanation: str | None = None


class ExamPaperSummaryResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    description: str | None = None
    item_count: int
    created_at: datetime
    updated_at: datetime


class ExamPaperResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    description: str | None = None
    created_at: datetime
    updated_at: datetime
    items: list[ExamPaperItemResponse]
