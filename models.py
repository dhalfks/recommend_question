from sqlalchemy import create_engine, Column, Integer, BigInteger, String, Text, Float, Numeric, Date, DateTime, ForeignKey, Enum, Boolean, func
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime
import enum

from config import settings

# Database 엔진 설정
# PostgreSQL 연결
engine = create_engine(
    settings.DATABASE_URL,
    echo=False,
    pool_pre_ping=True,  # 연결 유효성 확인
    pool_recycle=3600,   # 1시간마다 연결 재생성
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Enum 정의
class DifficultyLevel(str, enum.Enum):
    EASY = "EASY"
    MEDIUM = "MEDIUM"
    HARD = "HARD"
    EXPERT = "EXPERT"

class QuestionType(str, enum.Enum):
    EXCEL = "EXCEL"
    CODE = "CODE"

class AnswerType(str, enum.Enum):
    MULTIPLE_CHOICE = "MULTIPLE_CHOICE"
    SUBJECTIVE = "SUBJECTIVE"
    CODE_INPUT = "CODE_INPUT"

class UserRole(str, enum.Enum):
    STUDENT = "STUDENT"
    PROFESSOR = "PROFESSOR"
    ADMIN = "ADMIN"

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    phone = Column(String(30), nullable=False)
    email = Column(String(255), unique=True, nullable=False, index=True)
    password_hash = Column(String(512), nullable=False)
    role = Column(Enum(UserRole), nullable=False, default=UserRole.STUDENT)
    affiliation = Column(String(255), nullable=True)
    academic_year = Column(Integer, nullable=True)
    course_name = Column(String(255), nullable=True)
    professor_id = Column(
        Integer, ForeignKey("users.id", ondelete="RESTRICT"), nullable=True, index=True
    )
    created_at = Column(DateTime, default=datetime.utcnow)

    professor = relationship(
        "User", remote_side=[id], foreign_keys=[professor_id], backref="students"
    )

# 데이터베이스 모델
class Subject(Base):
    __tablename__ = "subjects"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, nullable=False)
    description = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # 관계
    questions = relationship("Question", back_populates="subject")

class Question(Base):
    __tablename__ = "questions"
    
    id = Column(Integer, primary_key=True, index=True)
    subject_id = Column(Integer, ForeignKey("subjects.id"), nullable=False)
    professor_id = Column(
        Integer, ForeignKey("users.id", ondelete="RESTRICT"), nullable=True, index=True
    )
    question_type = Column(Enum(QuestionType), nullable=False)
    answer_type = Column(Enum(AnswerType), nullable=False, default=AnswerType.MULTIPLE_CHOICE, server_default=AnswerType.MULTIPLE_CHOICE.value)
    title = Column(String(255), nullable=False)
    content = Column(Text, nullable=False)
    correct_answer = Column(Text, nullable=True)
    explanation = Column(Text, nullable=True)
    difficulty = Column(Enum(DifficultyLevel), nullable=False)
    source_file = Column(String(255), nullable=True)  # 코드 기반 문제의 원본 파일
    options = Column(Text, nullable=True)  # JSON 형식의 객관식 선택지
    tags = Column(Text, nullable=True)  # 쉼표로 구분된 태그
    external_id = Column(Integer, nullable=True, index=True)  # Excel 원본 id
    subject_code = Column(String(50), nullable=True, index=True)
    subject_unit = Column(String(255), nullable=True)
    code_snippet = Column(Text, nullable=True)
    answer_code_snippet = Column(Text, nullable=True)
    benchmark_time = Column(Integer, nullable=True)
    correct_option = Column(Integer, nullable=True)  # Excel 원본 정답 번호(1~4)
    is_required = Column(Boolean, nullable=False, default=False, server_default="false", index=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # 관계
    subject = relationship("Subject", back_populates="questions")
    professor = relationship("User", foreign_keys=[professor_id])

class ExcelQuestion(Base):
    __tablename__ = "excel_questions"
    
    id = Column(Integer, primary_key=True, index=True)
    question_id = Column(Integer, ForeignKey("questions.id"), nullable=False)
    excel_row_number = Column(Integer, nullable=False)
    file_name = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

class CodeFile(Base):
    __tablename__ = "code_files"
    
    id = Column(Integer, primary_key=True, index=True)
    file_name = Column(String(255), nullable=False)
    file_path = Column(String(500), nullable=False)
    file_type = Column(String(20), nullable=False)  # java, js, sql, txt, md
    file_content = Column(Text, nullable=False)
    subject_id = Column(Integer, ForeignKey("subjects.id"), nullable=True)
    professor_id = Column(
        Integer, ForeignKey("users.id", ondelete="RESTRICT"), nullable=True, index=True
    )
    uploaded_at = Column(DateTime, default=datetime.utcnow)
    
    # 관계
    subject = relationship("Subject")
    professor = relationship("User", foreign_keys=[professor_id])

class UserProgress(Base):
    __tablename__ = "user_progress"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String(100), nullable=False)
    question_id = Column(Integer, ForeignKey("questions.id"), nullable=False)
    is_correct = Column(String(20), nullable=True)  # "CORRECT", "INCORRECT", "SKIP"
    user_answer = Column(Text, nullable=True)
    session_id = Column(String(36), nullable=True, index=True)
    sequence_number = Column(Integer, nullable=True)
    elapsed_seconds = Column(Float, nullable=True)
    achievement_score = Column(Float, nullable=True)
    attempted_at = Column(DateTime, default=datetime.utcnow)

class QuizSession(Base):
    __tablename__ = "quiz_sessions"

    id = Column(String(36), primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    total_seconds = Column(Float, nullable=False)
    total_questions = Column(Integer, nullable=False)
    correct_answers = Column(Integer, nullable=False)
    score_percent = Column(Float, nullable=False)
    achievement_score = Column(Float, nullable=False)
    completed_at = Column(DateTime, default=datetime.utcnow)


class PublicExam(Base):
    __tablename__ = "public_exams"

    id = Column(BigInteger, primary_key=True)
    code = Column(String(64), nullable=False, unique=True)
    name = Column(String(200), nullable=False)
    description = Column(Text, nullable=True)
    is_active = Column(Boolean, nullable=False, server_default="true")
    created_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
    updated_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())

    rounds = relationship("PublicExamRound", back_populates="exam")


class PublicExamRound(Base):
    __tablename__ = "public_exam_rounds"

    id = Column(BigInteger, primary_key=True)
    exam_id = Column(
        BigInteger, ForeignKey("public_exams.id", ondelete="RESTRICT"), nullable=False
    )
    exam_year = Column(Integer, nullable=False)
    round_identifier = Column(String(100), nullable=False)
    display_name = Column(String(255), nullable=True)
    held_on = Column(Date, nullable=True)
    is_published = Column(Boolean, nullable=False, server_default="false")
    created_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
    updated_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())

    exam = relationship("PublicExam", back_populates="rounds")
    subjects = relationship("PublicExamSubject", back_populates="round")
    source_documents = relationship("PublicExamSourceDocument", back_populates="round")


class PublicExamSubject(Base):
    __tablename__ = "public_exam_subjects"

    id = Column(BigInteger, primary_key=True)
    round_id = Column(
        BigInteger,
        ForeignKey("public_exam_rounds.id", ondelete="RESTRICT"),
        nullable=False,
    )
    code = Column(String(64), nullable=True)
    name = Column(String(200), nullable=False)
    display_order = Column(Integer, nullable=False)
    created_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
    updated_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())

    round = relationship("PublicExamRound", back_populates="subjects")
    questions = relationship("PublicExamQuestion", back_populates="subject")


class PublicExamSourceDocument(Base):
    __tablename__ = "public_exam_source_documents"

    id = Column(BigInteger, primary_key=True)
    round_id = Column(
        BigInteger,
        ForeignKey("public_exam_rounds.id", ondelete="RESTRICT"),
        nullable=False,
    )
    original_file_name = Column(String(500), nullable=False)
    storage_key = Column(String(1000), nullable=True)
    source_url = Column(Text, nullable=True)
    source_organization = Column(String(255), nullable=True)
    source_notes = Column(Text, nullable=True)
    sha256 = Column(String(64), nullable=True)
    uploaded_by = Column(
        Integer, ForeignKey("users.id", ondelete="RESTRICT"), nullable=False
    )
    uploaded_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())

    round = relationship("PublicExamRound", back_populates="source_documents")
    uploader = relationship("User", foreign_keys=[uploaded_by])


class PublicExamQuestion(Base):
    __tablename__ = "public_exam_questions"

    id = Column(BigInteger, primary_key=True)
    subject_id = Column(
        BigInteger,
        ForeignKey("public_exam_subjects.id", ondelete="RESTRICT"),
        nullable=False,
    )
    source_document_id = Column(
        BigInteger,
        ForeignKey("public_exam_source_documents.id", ondelete="RESTRICT"),
        nullable=True,
    )
    question_number = Column(Integer, nullable=False)
    content = Column(Text, nullable=False)
    options = Column(JSONB, nullable=True)
    question_type = Column(
        String(32), nullable=False, server_default="MULTIPLE_CHOICE"
    )
    correct_option = Column(Integer, nullable=True)
    correct_answer = Column(Text, nullable=True)
    explanation = Column(Text, nullable=True)
    source_page = Column(Integer, nullable=True)
    answer_verification_status = Column(
        String(16), nullable=False, server_default="MISSING"
    )
    publication_status = Column(String(16), nullable=False, server_default="DRAFT")
    review_notes = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
    updated_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())

    subject = relationship("PublicExamSubject", back_populates="questions")
    source_document = relationship("PublicExamSourceDocument")


class PublicExamAttempt(Base):
    __tablename__ = "public_exam_attempts"

    id = Column(UUID(as_uuid=True), primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="RESTRICT"), nullable=False)
    subject_id = Column(
        BigInteger,
        ForeignKey("public_exam_subjects.id", ondelete="RESTRICT"),
        nullable=False,
    )
    status = Column(String(16), nullable=False, server_default="IN_PROGRESS")
    started_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
    last_activity_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
    submitted_at = Column(DateTime(timezone=True), nullable=True)
    abandoned_at = Column(DateTime(timezone=True), nullable=True)
    total_elapsed_seconds = Column(BigInteger, nullable=True)
    total_questions = Column(Integer, nullable=True)
    correct_answers = Column(Integer, nullable=True)
    incorrect_answers = Column(Integer, nullable=True)
    score_percent = Column(Numeric(5, 2), nullable=True)
    created_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
    updated_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())


class PublicExamAttemptAnswer(Base):
    __tablename__ = "public_exam_attempt_answers"

    id = Column(BigInteger, primary_key=True)
    attempt_id = Column(
        UUID(as_uuid=True),
        ForeignKey("public_exam_attempts.id", ondelete="CASCADE"),
        nullable=False,
    )
    question_id = Column(
        BigInteger,
        ForeignKey("public_exam_questions.id", ondelete="RESTRICT"),
        nullable=False,
    )
    sequence_number = Column(Integer, nullable=False)
    selected_option = Column(Integer, nullable=True)
    written_answer = Column(Text, nullable=True)
    elapsed_seconds = Column(Numeric(12, 3), nullable=False, server_default="0")
    is_correct = Column(Boolean, nullable=True)
    answered_at = Column(DateTime(timezone=True), nullable=True)
    graded_at = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
    updated_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())

# 테이블 생성
def create_tables():
    Base.metadata.create_all(bind=engine)
    # create_all은 기존 테이블에 새 컬럼을 추가하지 않으므로 가벼운 호환 마이그레이션을 수행한다.
    from sqlalchemy import inspect, text
    columns = {column["name"] for column in inspect(engine).get_columns("questions")}
    if "answer_code_snippet" not in columns:
        with engine.begin() as connection:
            connection.execute(
                text("ALTER TABLE questions ADD COLUMN answer_code_snippet TEXT")
            )
    if "answer_type" not in columns:
        with engine.begin() as connection:
            connection.execute(text("CREATE TYPE answertype AS ENUM ('MULTIPLE_CHOICE', 'SUBJECTIVE', 'CODE_INPUT')"))
            connection.execute(text("ALTER TABLE questions ADD COLUMN answer_type answertype NOT NULL DEFAULT 'MULTIPLE_CHOICE'"))
            connection.execute(text("UPDATE questions SET answer_type = CASE WHEN options IS NULL OR BTRIM(options) IN ('', '[]') THEN 'SUBJECTIVE'::answertype ELSE 'MULTIPLE_CHOICE'::answertype END"))
    if "is_required" not in columns:
        with engine.begin() as connection:
            connection.execute(
                text("ALTER TABLE questions ADD COLUMN is_required BOOLEAN NOT NULL DEFAULT FALSE")
            )
            connection.execute(
                text("CREATE INDEX IF NOT EXISTS idx_questions_is_required ON questions(is_required)")
            )
    progress_columns = {
        column["name"] for column in inspect(engine).get_columns("user_progress")
    }
    progress_column_types = {
        "session_id": "VARCHAR(36)",
        "sequence_number": "INTEGER",
        "elapsed_seconds": "FLOAT",
        "achievement_score": "FLOAT",
    }
    with engine.begin() as connection:
        for name, sql_type in progress_column_types.items():
            if name not in progress_columns:
                connection.execute(
                    text(f"ALTER TABLE user_progress ADD COLUMN {name} {sql_type}")
                )

# DB 세션 의존성
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
