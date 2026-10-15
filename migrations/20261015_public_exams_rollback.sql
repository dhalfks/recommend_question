-- Draft only: rollback for 20261015_public_exams.sql
-- WARNING: running this rollback permanently removes all common-exam data.
-- Do not run without an approved backup and explicit confirmation.

BEGIN;

DROP TABLE IF EXISTS public_exam_attempt_answers;
DROP TABLE IF EXISTS public_exam_attempts;
DROP TABLE IF EXISTS public_exam_questions;
DROP TABLE IF EXISTS public_exam_source_documents;
DROP TABLE IF EXISTS public_exam_subjects;
DROP TABLE IF EXISTS public_exam_rounds;
DROP TABLE IF EXISTS public_exams;

COMMIT;
