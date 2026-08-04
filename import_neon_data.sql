\set ON_ERROR_STOP on

-- WARNING: This replaces the current application data in the target database.
BEGIN;

TRUNCATE TABLE
    public.user_progress,
    public.excel_questions,
    public.quiz_sessions,
    public.code_files,
    public.questions,
    public.subjects,
    public.users
RESTART IDENTITY CASCADE;

\ir neon_data_inserts.sql

COMMIT;
