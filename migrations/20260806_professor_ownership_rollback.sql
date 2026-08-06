BEGIN;

DROP TRIGGER IF EXISTS trg_code_files_validate_professor ON code_files;
DROP TRIGGER IF EXISTS trg_questions_validate_professor ON questions;
DROP TRIGGER IF EXISTS trg_users_validate_professor ON users;
DROP FUNCTION IF EXISTS validate_professor_reference();

ALTER TABLE code_files
    DROP CONSTRAINT IF EXISTS code_files_professor_id_fkey,
    DROP COLUMN IF EXISTS professor_id;

ALTER TABLE questions
    DROP CONSTRAINT IF EXISTS questions_professor_id_fkey,
    DROP COLUMN IF EXISTS professor_id;

ALTER TABLE users
    DROP CONSTRAINT IF EXISTS users_student_professor_check,
    DROP CONSTRAINT IF EXISTS users_professor_id_fkey,
    DROP COLUMN IF EXISTS professor_id,
    DROP COLUMN IF EXISTS course_name,
    DROP COLUMN IF EXISTS academic_year,
    DROP COLUMN IF EXISTS affiliation;

COMMIT;
