BEGIN;

CREATE TABLE exam_papers (
    id BIGSERIAL PRIMARY KEY,
    professor_id INTEGER NOT NULL REFERENCES users(id) ON DELETE RESTRICT,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    CONSTRAINT exam_papers_title_not_blank CHECK (BTRIM(title) <> '')
);

CREATE TABLE exam_paper_items (
    id BIGSERIAL PRIMARY KEY,
    exam_paper_id BIGINT NOT NULL REFERENCES exam_papers(id) ON DELETE CASCADE,
    question_id INTEGER NOT NULL REFERENCES questions(id) ON DELETE RESTRICT,
    display_order INTEGER NOT NULL,
    subject_id INTEGER NOT NULL REFERENCES subjects(id) ON DELETE RESTRICT,
    subject_name VARCHAR(100) NOT NULL,
    title VARCHAR(255) NOT NULL,
    content TEXT NOT NULL,
    answer_type VARCHAR(32) NOT NULL,
    options JSONB,
    code_snippet TEXT,
    correct_answer TEXT,
    correct_option INTEGER,
    explanation TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    CONSTRAINT exam_paper_items_order_positive CHECK (display_order > 0),
    CONSTRAINT exam_paper_items_answer_type_valid CHECK (
        answer_type IN ('MULTIPLE_CHOICE', 'SUBJECTIVE', 'CODE_INPUT')
    ),
    CONSTRAINT exam_paper_items_options_array CHECK (
        options IS NULL OR jsonb_typeof(options) = 'array'
    ),
    CONSTRAINT exam_paper_items_correct_option_valid CHECK (
        correct_option IS NULL OR correct_option BETWEEN 1 AND 4
    ),
    CONSTRAINT uq_exam_paper_item_order UNIQUE (exam_paper_id, display_order),
    CONSTRAINT uq_exam_paper_item_question UNIQUE (exam_paper_id, question_id)
);

CREATE OR REPLACE FUNCTION validate_exam_paper_professor()
RETURNS trigger
LANGUAGE plpgsql
AS $$
BEGIN
    IF NOT EXISTS (
        SELECT 1 FROM users
        WHERE id = NEW.professor_id AND role::text = 'PROFESSOR'
    ) THEN
        RAISE EXCEPTION 'professor_id % does not reference a professor', NEW.professor_id;
    END IF;
    RETURN NEW;
END;
$$;

CREATE TRIGGER trg_exam_papers_validate_professor
BEFORE INSERT OR UPDATE OF professor_id ON exam_papers
FOR EACH ROW EXECUTE FUNCTION validate_exam_paper_professor();

CREATE INDEX idx_exam_papers_professor_updated
    ON exam_papers (professor_id, updated_at DESC);
CREATE INDEX idx_exam_paper_items_paper_order
    ON exam_paper_items (exam_paper_id, display_order);
CREATE INDEX idx_exam_paper_items_question_id
    ON exam_paper_items (question_id);

COMMIT;
