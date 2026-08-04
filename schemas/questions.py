from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List
from enum import Enum

# Enum
class DifficultyEnum(str, Enum):
    EASY = "EASY"
    MEDIUM = "MEDIUM"
    HARD = "HARD"
    EXPERT = "EXPERT"

class QuestionTypeEnum(str, Enum):
    EXCEL = "EXCEL"
    CODE = "CODE"

# Subject 스키마
class SubjectCreate(BaseModel):
    name: str
    description: Optional[str] = None

class SubjectUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None

class SubjectResponse(BaseModel):
    id: int
    name: str
    description: Optional[str]
    created_at: datetime
    
    class Config:
        from_attributes = True

# Question 스키마
class QuestionCreate(BaseModel):
    subject_id: int
    title: str
    content: str
    correct_answer: Optional[str] = None
    explanation: Optional[str] = None
    difficulty: DifficultyEnum
    source_file: Optional[str] = None
    options: Optional[str] = None
    tags: Optional[str] = None
    code_snippet: Optional[str] = None
    answer_code_snippet: Optional[str] = None
    is_required: bool = False

class QuestionUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    correct_answer: Optional[str] = None
    explanation: Optional[str] = None
    difficulty: Optional[DifficultyEnum] = None
    options: Optional[str] = None
    tags: Optional[str] = None
    code_snippet: Optional[str] = None
    answer_code_snippet: Optional[str] = None
    is_required: Optional[bool] = None

class QuestionResponse(BaseModel):
    id: int
    subject_id: int
    question_type: QuestionTypeEnum
    title: str
    content: str
    correct_answer: Optional[str]
    explanation: Optional[str]
    difficulty: DifficultyEnum
    source_file: Optional[str]
    options: Optional[str]
    tags: Optional[str]
    external_id: Optional[int] = None
    subject_code: Optional[str] = None
    subject_unit: Optional[str] = None
    code_snippet: Optional[str] = None
    answer_code_snippet: Optional[str] = None
    benchmark_time: Optional[int] = None
    correct_option: Optional[int] = None
    is_required: bool = False
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

class RandomQuestionsRequest(BaseModel):
    subject_id: Optional[int] = None
    subject_unit: Optional[str] = None
    difficulty: Optional[DifficultyEnum] = None
    count: int = 5

class RandomQuestionsResponse(BaseModel):
    questions: List[QuestionResponse]
    total_count: int
