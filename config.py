import os
from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    # Database (로컬 PostgreSQL)
    DATABASE_URL: str
    
    # OpenAI API
    OPENAI_API_KEY: str = ""
    OPENAI_MODEL: str = "gpt-5.6-sol"
    OPENAI_GRADING_MODEL: str = "gpt-5.6-luna"
    OPENAI_GRADING_REVIEW_MODEL: str = "gpt-5.6-sol"
    OPENAI_GRADING_CONFIDENCE_THRESHOLD: float = 0.75
    
    # Server
    SERVER_HOST: str = "0.0.0.0"
    SERVER_PORT: int = 8000

    # Authentication
    JWT_SECRET_KEY: str
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = 480
    ADMIN_SIGNUP_CODE: str = ""
    
    # File Upload
    UPLOAD_DIR: str = "uploads"
    MAX_FILE_SIZE: int = 10 * 1024 * 1024  # 10MB
    ALLOWED_FILE_EXTENSIONS: list = [".java", ".js", ".sql", ".txt", ".md", ".xlsx", ".xls"]
    PUBLIC_EXAM_DOCUMENT_STORAGE: str = "auto"  # auto, local, or vercel_blob
    PUBLIC_EXAM_DOCUMENT_DIR: str = "uploads/public-exams"
    PUBLIC_EXAM_PDF_MAX_BYTES: int = 4 * 1024 * 1024
    BLOB_READ_WRITE_TOKEN: str = ""
    
    # CORS
    CORS_ORIGINS: list = ["http://localhost:3000", "https://yourfrontend.vercel.app"]
    
    class Config:
        env_file = ".env"
        case_sensitive = True
        extra = "allow"

settings = Settings()
