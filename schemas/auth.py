from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr, Field, model_validator

from models import UserRole


class RegisterRequest(BaseModel):
    name: str = Field(min_length=2, max_length=100)
    phone: str = Field(min_length=7, max_length=30)
    email: EmailStr
    password: str = Field(min_length=8, max_length=128)
    role: UserRole
    affiliation: Optional[str] = Field(default=None, max_length=255)
    academic_year: Optional[int] = Field(default=None, ge=2000, le=2100)
    course_name: Optional[str] = Field(default=None, max_length=255)
    professor_id: Optional[int] = None
    admin_signup_code: Optional[str] = None

    @model_validator(mode="after")
    def validate_organization(self):
        if self.role in (UserRole.STUDENT, UserRole.PROFESSOR):
            if not self.affiliation or not self.affiliation.strip():
                raise ValueError("소속을 입력해 주세요.")
            if not self.course_name or not self.course_name.strip():
                raise ValueError("과정명을 입력해 주세요.")
        if self.role == UserRole.STUDENT:
            if self.academic_year is None:
                raise ValueError("연도를 입력해 주세요.")
            if self.professor_id is None:
                raise ValueError("담당 교수자를 선택해 주세요.")
        elif self.professor_id is not None:
            raise ValueError("학생만 담당 교수자를 지정할 수 있습니다.")
        return self


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class UserUpdateRequest(BaseModel):
    name: Optional[str] = Field(default=None, min_length=2, max_length=100)
    phone: Optional[str] = Field(default=None, min_length=7, max_length=30)
    email: Optional[EmailStr] = None
    current_password: Optional[str] = None
    new_password: Optional[str] = Field(default=None, min_length=8, max_length=128)
    affiliation: Optional[str] = Field(default=None, max_length=255)
    academic_year: Optional[int] = Field(default=None, ge=2000, le=2100)
    course_name: Optional[str] = Field(default=None, max_length=255)


class UserResponse(BaseModel):
    id: int
    name: str
    phone: str
    email: EmailStr
    role: UserRole
    affiliation: Optional[str] = None
    academic_year: Optional[int] = None
    course_name: Optional[str] = None
    professor_id: Optional[int] = None
    created_at: datetime

    class Config:
        from_attributes = True


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserResponse


class ProfessorResponse(BaseModel):
    id: int
    name: str
    affiliation: Optional[str] = None
    course_name: Optional[str] = None

    class Config:
        from_attributes = True
