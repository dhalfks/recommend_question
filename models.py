from sqlalchemy import create_engine, Column, Integer, BigInteger, String, Text, Float, Numeric, Date, DateTime, ForeignKey, Enum, Boolean, CheckConstraint, Index, UniqueConstraint, func, text
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


class BillingPlan(Base):
    __tablename__ = "billing_plans"
    __table_args__ = (
        CheckConstraint("BTRIM(code) <> ''", name="billing_plans_code_not_blank"),
        CheckConstraint(
            "audience_role IN ('STUDENT', 'PROFESSOR')",
            name="billing_plans_audience_role_valid",
        ),
        CheckConstraint("price > 0", name="billing_plans_price_positive"),
        CheckConstraint("currency = 'KRW'", name="billing_plans_currency_valid"),
        CheckConstraint(
            "billing_period IN ('ONE_TIME', 'MONTHLY')",
            name="billing_plans_period_valid",
        ),
        CheckConstraint(
            "entitlement_days > 0", name="billing_plans_entitlement_days_positive"
        ),
        CheckConstraint(
            "jsonb_typeof(features) = 'object'", name="billing_plans_features_object"
        ),
    )

    id = Column(BigInteger, primary_key=True)
    code = Column(String(50), nullable=False, unique=True)
    name = Column(String(100), nullable=False)
    audience_role = Column(String(20), nullable=False)
    price = Column(BigInteger, nullable=False)
    currency = Column(String(3), nullable=False, server_default="KRW")
    billing_period = Column(String(20), nullable=False)
    entitlement_days = Column(Integer, nullable=False)
    features = Column(JSONB, nullable=False, server_default="{}")
    is_active = Column(Boolean, nullable=False, server_default="true")
    created_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
    updated_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())


class BillingCustomer(Base):
    __tablename__ = "billing_customers"
    __table_args__ = (
        CheckConstraint(
            "CHAR_LENGTH(customer_key) BETWEEN 10 AND 50",
            name="billing_customers_key_length",
        ),
        CheckConstraint(
            "customer_key ~ '^[A-Za-z0-9._=@-]+$'",
            name="billing_customers_key_format",
        ),
    )

    id = Column(BigInteger, primary_key=True)
    user_id = Column(
        Integer, ForeignKey("users.id", ondelete="RESTRICT"), nullable=False, unique=True
    )
    customer_key = Column(String(50), nullable=False, unique=True)
    created_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())

    user = relationship("User", foreign_keys=[user_id])


class UserSubscription(Base):
    __tablename__ = "user_subscriptions"
    __table_args__ = (
        CheckConstraint(
            "status IN ('PENDING', 'ACTIVE', 'PAST_DUE', 'CANCELED', 'EXPIRED')",
            name="user_subscriptions_status_valid",
        ),
        CheckConstraint(
            "current_period_end IS NULL OR current_period_start IS NULL "
            "OR current_period_end > current_period_start",
            name="user_subscriptions_period_valid",
        ),
        Index(
            "uq_user_subscriptions_active_plan",
            "user_id",
            "plan_id",
            unique=True,
            postgresql_where=text("status = 'ACTIVE'"),
        ),
        Index(
            "idx_user_subscriptions_user_status_end",
            "user_id",
            "status",
            text("current_period_end DESC"),
        ),
    )

    id = Column(BigInteger, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="RESTRICT"), nullable=False)
    plan_id = Column(
        BigInteger, ForeignKey("billing_plans.id", ondelete="RESTRICT"), nullable=False
    )
    status = Column(String(20), nullable=False)
    started_at = Column(DateTime(timezone=True), nullable=True)
    current_period_start = Column(DateTime(timezone=True), nullable=True)
    current_period_end = Column(DateTime(timezone=True), nullable=True)
    cancel_at_period_end = Column(Boolean, nullable=False, server_default="false")
    canceled_at = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
    updated_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())

    user = relationship("User", foreign_keys=[user_id])
    plan = relationship("BillingPlan", foreign_keys=[plan_id])


class PaymentOrder(Base):
    __tablename__ = "payment_orders"
    __table_args__ = (
        CheckConstraint("amount > 0", name="payment_orders_amount_positive"),
        CheckConstraint("currency = 'KRW'", name="payment_orders_currency_valid"),
        CheckConstraint(
            "status IN ('READY', 'PAID', 'FAILED', 'CANCELED', 'REFUNDED')",
            name="payment_orders_status_valid",
        ),
        CheckConstraint("provider = 'TOSS'", name="payment_orders_provider_valid"),
        Index("idx_payment_orders_user_created", "user_id", text("created_at DESC")),
        Index("idx_payment_orders_status_created", "status", "created_at"),
    )

    id = Column(BigInteger, primary_key=True)
    order_id = Column(String(100), nullable=False, unique=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="RESTRICT"), nullable=False)
    plan_id = Column(
        BigInteger, ForeignKey("billing_plans.id", ondelete="RESTRICT"), nullable=False
    )
    subscription_id = Column(
        BigInteger,
        ForeignKey("user_subscriptions.id", ondelete="RESTRICT"),
        nullable=True,
    )
    plan_code = Column(String(50), nullable=False)
    plan_name = Column(String(100), nullable=False)
    amount = Column(BigInteger, nullable=False)
    currency = Column(String(3), nullable=False, server_default="KRW")
    status = Column(String(20), nullable=False, server_default="READY")
    provider = Column(String(20), nullable=False, server_default="TOSS")
    failure_code = Column(String(100), nullable=True)
    failure_message = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
    paid_at = Column(DateTime(timezone=True), nullable=True)
    canceled_at = Column(DateTime(timezone=True), nullable=True)
    updated_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())

    user = relationship("User", foreign_keys=[user_id])
    plan = relationship("BillingPlan", foreign_keys=[plan_id])
    subscription = relationship("UserSubscription", foreign_keys=[subscription_id])


class PaymentTransaction(Base):
    __tablename__ = "payment_transactions"
    __table_args__ = (
        CheckConstraint(
            "transaction_type IN ('PAYMENT', 'REFUND')",
            name="payment_transactions_type_valid",
        ),
        CheckConstraint(
            "status IN ('PENDING', 'SUCCEEDED', 'FAILED')",
            name="payment_transactions_status_valid",
        ),
        CheckConstraint("amount > 0", name="payment_transactions_amount_positive"),
        CheckConstraint("currency = 'KRW'", name="payment_transactions_currency_valid"),
        CheckConstraint(
            "provider_response IS NULL OR jsonb_typeof(provider_response) = 'object'",
            name="payment_transactions_provider_response_object",
        ),
        Index(
            "uq_payment_transactions_provider_payment_success",
            "provider_payment_id",
            "transaction_type",
            unique=True,
            postgresql_where=text(
                "provider_payment_id IS NOT NULL AND status = 'SUCCEEDED'"
            ),
        ),
        Index(
            "idx_payment_transactions_order_created",
            "payment_order_id",
            "created_at",
        ),
    )

    id = Column(BigInteger, primary_key=True)
    payment_order_id = Column(
        BigInteger, ForeignKey("payment_orders.id", ondelete="RESTRICT"), nullable=False
    )
    provider_payment_id = Column(String(200), nullable=True)
    transaction_type = Column(String(20), nullable=False)
    status = Column(String(20), nullable=False)
    amount = Column(BigInteger, nullable=False)
    currency = Column(String(3), nullable=False, server_default="KRW")
    idempotency_key = Column(String(100), nullable=False, unique=True)
    provider_response = Column(JSONB, nullable=True)
    failure_code = Column(String(100), nullable=True)
    failure_message = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())

    order = relationship("PaymentOrder", foreign_keys=[payment_order_id])


class RefundRequest(Base):
    __tablename__ = "refund_requests"
    __table_args__ = (
        CheckConstraint(
            "status IN ('PENDING', 'APPROVED', 'REJECTED')",
            name="refund_requests_status_valid",
        ),
        CheckConstraint("BTRIM(reason) <> ''", name="refund_requests_reason_not_blank"),
        CheckConstraint(
            "jsonb_typeof(eligibility_snapshot) = 'object'",
            name="refund_requests_snapshot_object",
        ),
        Index(
            "uq_refund_requests_pending_order",
            "order_id",
            unique=True,
            postgresql_where=text("status = 'PENDING'"),
        ),
        Index("idx_refund_requests_user_requested", "user_id", text("requested_at DESC")),
        Index("idx_refund_requests_status_requested", "status", "requested_at"),
    )

    id = Column(BigInteger, primary_key=True)
    order_id = Column(
        BigInteger, ForeignKey("payment_orders.id", ondelete="RESTRICT"), nullable=False
    )
    user_id = Column(Integer, ForeignKey("users.id", ondelete="RESTRICT"), nullable=False)
    status = Column(String(20), nullable=False, server_default="PENDING")
    reason = Column(Text, nullable=False)
    eligibility_snapshot = Column(JSONB, nullable=False)
    decision_reason = Column(Text, nullable=True)
    reviewed_by = Column(Integer, ForeignKey("users.id", ondelete="RESTRICT"), nullable=True)
    refund_transaction_id = Column(
        BigInteger,
        ForeignKey("payment_transactions.id", ondelete="RESTRICT"),
        nullable=True,
    )
    requested_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
    reviewed_at = Column(DateTime(timezone=True), nullable=True)
    updated_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())

    order = relationship("PaymentOrder", foreign_keys=[order_id])
    user = relationship("User", foreign_keys=[user_id])
    reviewer = relationship("User", foreign_keys=[reviewed_by])
    refund_transaction = relationship("PaymentTransaction", foreign_keys=[refund_transaction_id])


class AIUsageEvent(Base):
    __tablename__ = "ai_usage_events"
    __table_args__ = (
        CheckConstraint(
            "feature_code IN ('AI_EXPLANATION', 'CODE_REVIEW', 'QUESTION_GENERATION')",
            name="ai_usage_events_feature_valid",
        ),
        CheckConstraint(
            "status IN ('STARTED', 'SUCCEEDED', 'FAILED')",
            name="ai_usage_events_status_valid",
        ),
        CheckConstraint(
            "input_tokens IS NULL OR input_tokens >= 0",
            name="ai_usage_events_input_tokens_nonnegative",
        ),
        CheckConstraint(
            "output_tokens IS NULL OR output_tokens >= 0",
            name="ai_usage_events_output_tokens_nonnegative",
        ),
        Index(
            "idx_ai_usage_events_user_feature_created",
            "user_id",
            "feature_code",
            text("created_at DESC"),
        ),
    )

    id = Column(BigInteger, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="RESTRICT"), nullable=False)
    feature_code = Column(String(50), nullable=False)
    subscription_id = Column(
        BigInteger,
        ForeignKey("user_subscriptions.id", ondelete="SET NULL"),
        nullable=True,
    )
    request_id = Column(String(100), nullable=False, unique=True)
    input_tokens = Column(Integer, nullable=True)
    output_tokens = Column(Integer, nullable=True)
    status = Column(String(20), nullable=False)
    failure_code = Column(String(100), nullable=True)
    created_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
    completed_at = Column(DateTime(timezone=True), nullable=True)

    user = relationship("User", foreign_keys=[user_id])
    subscription = relationship("UserSubscription", foreign_keys=[subscription_id])


class PaymentWebhookEvent(Base):
    __tablename__ = "payment_webhook_events"
    __table_args__ = (
        UniqueConstraint(
            "provider", "event_id", name="uq_payment_webhook_provider_event"
        ),
        CheckConstraint("provider = 'TOSS'", name="payment_webhook_provider_valid"),
        CheckConstraint(
            "status IN ('RECEIVED', 'PROCESSED', 'FAILED')",
            name="payment_webhook_status_valid",
        ),
        CheckConstraint(
            "jsonb_typeof(payload) = 'object'", name="payment_webhook_payload_object"
        ),
        Index(
            "idx_payment_webhook_events_status_received", "status", "received_at"
        ),
    )

    id = Column(BigInteger, primary_key=True)
    provider = Column(String(20), nullable=False, server_default="TOSS")
    event_id = Column(String(200), nullable=False)
    event_type = Column(String(100), nullable=False)
    status = Column(String(20), nullable=False, server_default="RECEIVED")
    payload = Column(JSONB, nullable=False)
    error_message = Column(Text, nullable=True)
    received_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
    processed_at = Column(DateTime(timezone=True), nullable=True)

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


class ExamPaper(Base):
    __tablename__ = "exam_papers"
    __table_args__ = (
        CheckConstraint("BTRIM(title) <> ''", name="exam_papers_title_not_blank"),
        Index("idx_exam_papers_professor_updated", "professor_id", "updated_at"),
    )

    id = Column(BigInteger, primary_key=True)
    professor_id = Column(
        Integer, ForeignKey("users.id", ondelete="RESTRICT"), nullable=False
    )
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
    updated_at = Column(
        DateTime(timezone=True), nullable=False, server_default=func.now(), onupdate=func.now()
    )

    professor = relationship("User", foreign_keys=[professor_id])
    items = relationship(
        "ExamPaperItem",
        back_populates="paper",
        cascade="all, delete-orphan",
        order_by="ExamPaperItem.display_order",
    )


class ExamPaperItem(Base):
    __tablename__ = "exam_paper_items"
    __table_args__ = (
        CheckConstraint("display_order > 0", name="exam_paper_items_order_positive"),
        CheckConstraint(
            "answer_type IN ('MULTIPLE_CHOICE', 'SUBJECTIVE', 'CODE_INPUT')",
            name="exam_paper_items_answer_type_valid",
        ),
        CheckConstraint(
            "options IS NULL OR jsonb_typeof(options) = 'array'",
            name="exam_paper_items_options_array",
        ),
        CheckConstraint(
            "correct_option IS NULL OR correct_option BETWEEN 1 AND 4",
            name="exam_paper_items_correct_option_valid",
        ),
        UniqueConstraint("exam_paper_id", "display_order", name="uq_exam_paper_item_order"),
        UniqueConstraint("exam_paper_id", "question_id", name="uq_exam_paper_item_question"),
        Index("idx_exam_paper_items_paper_order", "exam_paper_id", "display_order"),
        Index("idx_exam_paper_items_question_id", "question_id"),
    )

    id = Column(BigInteger, primary_key=True)
    exam_paper_id = Column(
        BigInteger, ForeignKey("exam_papers.id", ondelete="CASCADE"), nullable=False
    )
    question_id = Column(
        Integer, ForeignKey("questions.id", ondelete="RESTRICT"), nullable=False
    )
    display_order = Column(Integer, nullable=False)
    subject_id = Column(Integer, ForeignKey("subjects.id", ondelete="RESTRICT"), nullable=False)
    subject_name = Column(String(100), nullable=False)
    title = Column(String(255), nullable=False)
    content = Column(Text, nullable=False)
    answer_type = Column(String(32), nullable=False)
    options = Column(JSONB, nullable=True)
    code_snippet = Column(Text, nullable=True)
    correct_answer = Column(Text, nullable=True)
    correct_option = Column(Integer, nullable=True)
    explanation = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())

    paper = relationship("ExamPaper", back_populates="items")
    question = relationship("Question")

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
