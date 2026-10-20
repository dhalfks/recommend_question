BEGIN;

DROP TRIGGER IF EXISTS trg_exam_papers_validate_professor ON exam_papers;
DROP FUNCTION IF EXISTS validate_exam_paper_professor();
DROP TABLE IF EXISTS exam_paper_items;
DROP TABLE IF EXISTS exam_papers;

COMMIT;
