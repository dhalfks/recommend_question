BEGIN;

DO $$
BEGIN
    IF NOT EXISTS (
        SELECT 1 FROM users WHERE id = 3 AND role::text = 'PROFESSOR'
    ) THEN
        RAISE EXCEPTION 'Legacy owner users.id=3 is not a professor';
    END IF;
END $$;

ALTER TABLE users
    ADD COLUMN IF NOT EXISTS affiliation VARCHAR(255),
    ADD COLUMN IF NOT EXISTS academic_year INTEGER,
    ADD COLUMN IF NOT EXISTS course_name VARCHAR(255),
    ADD COLUMN IF NOT EXISTS professor_id INTEGER;

ALTER TABLE questions
    ADD COLUMN IF NOT EXISTS professor_id INTEGER;

ALTER TABLE code_files
    ADD COLUMN IF NOT EXISTS professor_id INTEGER;

UPDATE users
SET
    affiliation = COALESCE(affiliation, '기존 데이터'),
    academic_year = COALESCE(academic_year, 2026),
    course_name = COALESCE(course_name, '기존 과정'),
    professor_id = CASE
        WHEN role::text = 'STUDENT' THEN COALESCE(professor_id, 3)
        ELSE NULL
    END;

UPDATE questions
SET professor_id = 3
WHERE professor_id IS NULL;

UPDATE code_files
SET professor_id = 3
WHERE professor_id IS NULL;

DO $$
BEGIN
    IF NOT EXISTS (
        SELECT 1 FROM pg_constraint
        WHERE conname = 'users_student_professor_check'
    ) THEN
        ALTER TABLE users
            ADD CONSTRAINT users_student_professor_check CHECK (
                (role::text = 'STUDENT' AND professor_id IS NOT NULL)
                OR (role::text <> 'STUDENT' AND professor_id IS NULL)
            );
    END IF;
END $$;

ALTER TABLE users DROP CONSTRAINT IF EXISTS users_professor_id_fkey;
ALTER TABLE users
    ADD CONSTRAINT users_professor_id_fkey
    FOREIGN KEY (professor_id) REFERENCES users(id) ON DELETE RESTRICT;

ALTER TABLE questions DROP CONSTRAINT IF EXISTS questions_professor_id_fkey;
ALTER TABLE questions
    ADD CONSTRAINT questions_professor_id_fkey
    FOREIGN KEY (professor_id) REFERENCES users(id) ON DELETE RESTRICT;

ALTER TABLE code_files DROP CONSTRAINT IF EXISTS code_files_professor_id_fkey;
ALTER TABLE code_files
    ADD CONSTRAINT code_files_professor_id_fkey
    FOREIGN KEY (professor_id) REFERENCES users(id) ON DELETE RESTRICT;

CREATE OR REPLACE FUNCTION validate_professor_reference()
RETURNS trigger
LANGUAGE plpgsql
AS $$
BEGIN
    IF NEW.professor_id IS NOT NULL AND NOT EXISTS (
        SELECT 1
        FROM users
        WHERE id = NEW.professor_id AND role::text = 'PROFESSOR'
    ) THEN
        RAISE EXCEPTION 'professor_id % does not reference a professor', NEW.professor_id;
    END IF;
    RETURN NEW;
END;
$$;

DROP TRIGGER IF EXISTS trg_users_validate_professor ON users;
CREATE TRIGGER trg_users_validate_professor
BEFORE INSERT OR UPDATE OF professor_id ON users
FOR EACH ROW EXECUTE FUNCTION validate_professor_reference();

DROP TRIGGER IF EXISTS trg_questions_validate_professor ON questions;
CREATE TRIGGER trg_questions_validate_professor
BEFORE INSERT OR UPDATE OF professor_id ON questions
FOR EACH ROW EXECUTE FUNCTION validate_professor_reference();

DROP TRIGGER IF EXISTS trg_code_files_validate_professor ON code_files;
CREATE TRIGGER trg_code_files_validate_professor
BEFORE INSERT OR UPDATE OF professor_id ON code_files
FOR EACH ROW EXECUTE FUNCTION validate_professor_reference();

CREATE INDEX IF NOT EXISTS idx_users_professor_id ON users(professor_id);
CREATE INDEX IF NOT EXISTS idx_questions_professor_id ON questions(professor_id);
CREATE INDEX IF NOT EXISTS idx_questions_professor_subject
    ON questions(professor_id, subject_id);
CREATE INDEX IF NOT EXISTS idx_code_files_professor_id ON code_files(professor_id);

COMMIT;
