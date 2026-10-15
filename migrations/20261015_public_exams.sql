-- Draft only: common certification past-exam schema
-- DO NOT run until the target Neon schema and application contract are approved.
-- This migration intentionally does not alter existing tables or seed data.

BEGIN;

CREATE TABLE public_exams (
    id BIGSERIAL PRIMARY KEY,
    code VARCHAR(64) NOT NULL UNIQUE,
    name VARCHAR(200) NOT NULL,
    description TEXT,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT public_exams_code_not_blank CHECK (BTRIM(code) <> ''),
    CONSTRAINT public_exams_name_not_blank CHECK (BTRIM(name) <> '')
);

CREATE TABLE public_exam_rounds (
    id BIGSERIAL PRIMARY KEY,
    exam_id BIGINT NOT NULL REFERENCES public_exams(id) ON DELETE RESTRICT,
    exam_year INTEGER NOT NULL,
    round_identifier VARCHAR(100) NOT NULL,
    display_name VARCHAR(255),
    held_on DATE,
    is_published BOOLEAN NOT NULL DEFAULT FALSE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT public_exam_rounds_year_valid CHECK (exam_year BETWEEN 1900 AND 2200),
    CONSTRAINT public_exam_rounds_identifier_not_blank
        CHECK (BTRIM(round_identifier) <> ''),
    CONSTRAINT uq_public_exam_round UNIQUE (exam_id, exam_year, round_identifier)
);

CREATE TABLE public_exam_subjects (
    id BIGSERIAL PRIMARY KEY,
    round_id BIGINT NOT NULL REFERENCES public_exam_rounds(id) ON DELETE RESTRICT,
    code VARCHAR(64),
    name VARCHAR(200) NOT NULL,
    display_order INTEGER NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT public_exam_subjects_name_not_blank CHECK (BTRIM(name) <> ''),
    CONSTRAINT public_exam_subjects_order_positive CHECK (display_order > 0),
    CONSTRAINT uq_public_exam_subject_name UNIQUE (round_id, name),
    CONSTRAINT uq_public_exam_subject_order UNIQUE (round_id, display_order)
);

CREATE TABLE public_exam_source_documents (
    id BIGSERIAL PRIMARY KEY,
    round_id BIGINT NOT NULL REFERENCES public_exam_rounds(id) ON DELETE RESTRICT,
    original_file_name VARCHAR(500) NOT NULL,
    storage_key VARCHAR(1000),
    source_url TEXT,
    source_organization VARCHAR(255),
    source_notes TEXT,
    sha256 CHAR(64),
    uploaded_by INTEGER NOT NULL REFERENCES users(id) ON DELETE RESTRICT,
    uploaded_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT public_exam_source_file_not_blank
        CHECK (BTRIM(original_file_name) <> ''),
    CONSTRAINT public_exam_source_sha256_format
        CHECK (sha256 IS NULL OR sha256 ~ '^[0-9a-fA-F]{64}$')
);

CREATE TABLE public_exam_questions (
    id BIGSERIAL PRIMARY KEY,
    subject_id BIGINT NOT NULL REFERENCES public_exam_subjects(id) ON DELETE RESTRICT,
    source_document_id BIGINT REFERENCES public_exam_source_documents(id) ON DELETE RESTRICT,
    question_number INTEGER NOT NULL,
    content TEXT NOT NULL,
    options JSONB,
    question_type VARCHAR(32) NOT NULL DEFAULT 'MULTIPLE_CHOICE',
    correct_option INTEGER,
    correct_answer TEXT,
    explanation TEXT,
    source_page INTEGER,
    answer_verification_status VARCHAR(16) NOT NULL DEFAULT 'MISSING',
    publication_status VARCHAR(16) NOT NULL DEFAULT 'DRAFT',
    review_notes TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT public_exam_questions_number_positive CHECK (question_number > 0),
    CONSTRAINT public_exam_questions_content_not_blank CHECK (BTRIM(content) <> ''),
    CONSTRAINT public_exam_questions_source_page_positive
        CHECK (source_page IS NULL OR source_page > 0),
    CONSTRAINT public_exam_questions_type_valid
        CHECK (question_type IN ('MULTIPLE_CHOICE', 'SHORT_ANSWER')),
    CONSTRAINT public_exam_questions_options_array
        CHECK (options IS NULL OR jsonb_typeof(options) = 'array'),
    CONSTRAINT public_exam_questions_answer_shape
        CHECK (
            (question_type = 'MULTIPLE_CHOICE' AND options IS NOT NULL AND jsonb_array_length(options) > 1 AND correct_answer IS NULL)
            OR
            (question_type = 'SHORT_ANSWER' AND options IS NULL AND correct_option IS NULL)
        ),
    CONSTRAINT public_exam_questions_correct_option_range
        CHECK (
            correct_option IS NULL
            OR (correct_option >= 1 AND correct_option <= jsonb_array_length(options))
        ),
    CONSTRAINT public_exam_questions_answer_status_valid
        CHECK (answer_verification_status IN ('MISSING', 'UNVERIFIED', 'VERIFIED')),
    CONSTRAINT public_exam_questions_missing_answer_is_null
        CHECK (
            answer_verification_status <> 'MISSING'
            OR (correct_option IS NULL AND correct_answer IS NULL)
        ),
    CONSTRAINT public_exam_questions_verified_answer_exists
        CHECK (
            answer_verification_status <> 'VERIFIED'
            OR correct_option IS NOT NULL
            OR NULLIF(BTRIM(correct_answer), '') IS NOT NULL
        ),
    CONSTRAINT public_exam_questions_publication_status_valid
        CHECK (publication_status IN ('DRAFT', 'READY', 'PUBLISHED', 'ARCHIVED')),
    CONSTRAINT public_exam_questions_publish_only_verified
        CHECK (
            publication_status <> 'PUBLISHED'
            OR answer_verification_status = 'VERIFIED'
        ),
    CONSTRAINT uq_public_exam_question_number UNIQUE (subject_id, question_number)
);

CREATE TABLE public_exam_attempts (
    id UUID PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE RESTRICT,
    subject_id BIGINT NOT NULL REFERENCES public_exam_subjects(id) ON DELETE RESTRICT,
    status VARCHAR(16) NOT NULL DEFAULT 'IN_PROGRESS',
    started_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    last_activity_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    submitted_at TIMESTAMPTZ,
    abandoned_at TIMESTAMPTZ,
    total_elapsed_seconds BIGINT,
    total_questions INTEGER,
    correct_answers INTEGER,
    incorrect_answers INTEGER,
    score_percent NUMERIC(5, 2),
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT public_exam_attempts_status_valid
        CHECK (status IN ('IN_PROGRESS', 'SUBMITTED', 'ABANDONED')),
    CONSTRAINT public_exam_attempts_time_order
        CHECK (
            submitted_at IS NULL OR submitted_at >= started_at
        ),
    CONSTRAINT public_exam_attempts_abandoned_time_order
        CHECK (
            abandoned_at IS NULL OR abandoned_at >= started_at
        ),
    CONSTRAINT public_exam_attempts_state_shape
        CHECK (
            (status = 'IN_PROGRESS' AND submitted_at IS NULL AND abandoned_at IS NULL AND total_elapsed_seconds IS NULL)
            OR
            (status = 'SUBMITTED' AND submitted_at IS NOT NULL AND abandoned_at IS NULL AND total_elapsed_seconds IS NOT NULL)
            OR
            (status = 'ABANDONED' AND submitted_at IS NULL AND abandoned_at IS NOT NULL)
        ),
    CONSTRAINT public_exam_attempts_elapsed_nonnegative
        CHECK (total_elapsed_seconds IS NULL OR total_elapsed_seconds >= 0),
    CONSTRAINT public_exam_attempts_counts_valid
        CHECK (
            (total_questions IS NULL OR total_questions >= 0)
            AND (correct_answers IS NULL OR correct_answers >= 0)
            AND (incorrect_answers IS NULL OR incorrect_answers >= 0)
            AND (score_percent IS NULL OR score_percent BETWEEN 0 AND 100)
            AND (total_questions IS NULL OR correct_answers IS NULL OR incorrect_answers IS NULL
                 OR total_questions = correct_answers + incorrect_answers)
        )
);

CREATE TABLE public_exam_attempt_answers (
    id BIGSERIAL PRIMARY KEY,
    attempt_id UUID NOT NULL REFERENCES public_exam_attempts(id) ON DELETE CASCADE,
    question_id BIGINT NOT NULL REFERENCES public_exam_questions(id) ON DELETE RESTRICT,
    sequence_number INTEGER NOT NULL,
    selected_option INTEGER,
    written_answer TEXT,
    elapsed_seconds NUMERIC(12, 3) NOT NULL DEFAULT 0,
    is_correct BOOLEAN,
    answered_at TIMESTAMPTZ,
    graded_at TIMESTAMPTZ,
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT public_exam_attempt_answers_sequence_positive CHECK (sequence_number > 0),
    CONSTRAINT public_exam_attempt_answers_elapsed_nonnegative CHECK (elapsed_seconds >= 0),
    CONSTRAINT public_exam_attempt_answers_one_answer_kind
        CHECK (NOT (selected_option IS NOT NULL AND written_answer IS NOT NULL)),
    CONSTRAINT uq_public_exam_attempt_question UNIQUE (attempt_id, question_id),
    CONSTRAINT uq_public_exam_attempt_sequence UNIQUE (attempt_id, sequence_number)
);

CREATE INDEX idx_public_exam_rounds_lookup
    ON public_exam_rounds (exam_id, is_published, exam_year DESC, round_identifier);
CREATE INDEX idx_public_exam_subjects_round
    ON public_exam_subjects (round_id, display_order);
CREATE INDEX idx_public_exam_sources_round
    ON public_exam_source_documents (round_id);
CREATE INDEX idx_public_exam_questions_subject_status
    ON public_exam_questions (subject_id, publication_status, question_number);
CREATE INDEX idx_public_exam_questions_review
    ON public_exam_questions (answer_verification_status, publication_status);
CREATE INDEX idx_public_exam_attempts_user_history
    ON public_exam_attempts (user_id, started_at DESC);
CREATE INDEX idx_public_exam_attempts_resume
    ON public_exam_attempts (user_id, subject_id, last_activity_at DESC)
    WHERE status = 'IN_PROGRESS';
CREATE INDEX idx_public_exam_attempt_answers_attempt
    ON public_exam_attempt_answers (attempt_id, sequence_number);
CREATE INDEX idx_public_exam_attempt_answers_wrong
    ON public_exam_attempt_answers (attempt_id, question_id)
    WHERE is_correct = FALSE;

COMMIT;
