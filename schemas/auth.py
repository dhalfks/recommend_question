from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr, Field

from models import UserRole


class RegisterRequest(BaseModel):
    name: str = Field(min_length=2, max_length=100)
    phone: str = Field(min_length=7, max_length=30)
    email: EmailStr
    password: str = Field(min_length=8, max_length=128)
    role: UserRole
    admin_signup_code: Optional[str] = None


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class UserUpdateRequest(BaseModel):
    name: Optional[str] = Field(default=None, min_length=2, max_length=100)
    phone: Optional[str] = Field(default=None, min_length=7, max_length=30)
    email: Optional[EmailStr] = None
    current_password: Optional[str] = None
    new_password: Optional[str] = Field(default=None, min_length=8, max_length=128)


class UserResponse(BaseModel):
    id: int
    name: str
    phone: str
    email: EmailStr
    role: UserRole
    created_at: datetime

    class Config:
        from_attributes = True


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserResponse
