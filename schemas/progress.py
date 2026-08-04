from typing import List, Optional, Union

from pydantic import BaseModel, Field


class QuizAnswer(BaseModel):
    question_id: int
    answer: Optional[Union[int, str]] = None
    sequence_number: int
    elapsed_seconds: float


class QuizSubmission(BaseModel):
    answers: List[QuizAnswer]
    session_id: Optional[str] = None
    total_seconds: float


class QuizSubmissionResult(BaseModel):
    attempted: int
    correct: int
    score_percent: int
    achievement_score: float
    session_id: str
    results: List[dict] = Field(default_factory=list)
