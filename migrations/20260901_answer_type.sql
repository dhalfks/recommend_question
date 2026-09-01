DO $$ BEGIN
    CREATE TYPE answertype AS ENUM ('MULTIPLE_CHOICE', 'SUBJECTIVE', 'CODE_INPUT');
EXCEPTION WHEN duplicate_object THEN NULL;
END $$;

ALTER TABLE questions ADD COLUMN IF NOT EXISTS answer_type answertype NOT NULL DEFAULT 'MULTIPLE_CHOICE';

UPDATE questions SET answer_type = CASE
    WHEN options IS NULL OR BTRIM(options) IN ('', '[]') THEN 'SUBJECTIVE'::answertype
    ELSE 'MULTIPLE_CHOICE'::answertype
END
WHERE answer_type = 'MULTIPLE_CHOICE';
