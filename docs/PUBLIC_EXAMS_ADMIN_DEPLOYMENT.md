# 공통 기출 관리자 배포 점검

## 저장소와 환경변수

- 로컬 개발: `PUBLIC_EXAM_DOCUMENT_STORAGE=local`, `PUBLIC_EXAM_DOCUMENT_DIR=uploads/public-exams`
- Vercel: Private Vercel Blob store를 프로젝트에 연결하고 `PUBLIC_EXAM_DOCUMENT_STORAGE=vercel_blob` 및 `BLOB_READ_WRITE_TOKEN`을 설정한다.
- `PUBLIC_EXAM_PDF_MAX_BYTES=4194304`가 기본값이다. Vercel Functions의 서버 업로드 본문 제한(4.5MB)보다 작게 유지한다.
- 통합 배포의 `NEXT_PUBLIC_API_URL=/api`, `DATABASE_URL`, `JWT_SECRET_KEY`, `CORS_ORIGINS`는 기존 방식대로 설정한다.
- 토큰과 DB 접속 문자열은 Git에 커밋하지 않는다.

Private Blob을 사용하므로 원본 PDF URL을 학생에게 반환하지 않는다. 원본 열람은 ADMIN Bearer 인증을 거치는 `/api/public-exams/admin/documents/{document_id}/file`로만 제공한다.

참고: [Vercel 서버 업로드](https://vercel.com/docs/vercel-blob/server-upload), [Vercel Private Blob](https://vercel.com/docs/vercel-blob/private-storage)

## 운영 스키마 읽기 전용 확인

아래 SQL은 읽기 전용 트랜잭션에서 7개 테이블과 핵심 컬럼을 확인한다. 결과 확인 후에도 `ROLLBACK`한다.

```sql
BEGIN TRANSACTION READ ONLY;

SELECT table_name
FROM information_schema.tables
WHERE table_schema = 'public'
  AND table_name IN (
    'public_exams', 'public_exam_rounds', 'public_exam_subjects',
    'public_exam_source_documents', 'public_exam_questions',
    'public_exam_attempts', 'public_exam_attempt_answers'
  )
ORDER BY table_name;

SELECT table_name, column_name, data_type, is_nullable, column_default
FROM information_schema.columns
WHERE table_schema = 'public'
  AND table_name IN ('public_exam_source_documents', 'public_exam_questions')
ORDER BY table_name, ordinal_position;

SELECT conrelid::regclass AS table_name, conname, pg_get_constraintdef(oid) AS definition
FROM pg_constraint
WHERE conrelid IN (
  'public_exam_source_documents'::regclass,
  'public_exam_questions'::regclass
)
ORDER BY table_name::text, conname;

SELECT tablename, indexname, indexdef
FROM pg_indexes
WHERE schemaname = 'public'
  AND tablename IN ('public_exam_source_documents', 'public_exam_questions')
ORDER BY tablename, indexname;

ROLLBACK;
```

이 구현은 기존 7개 테이블만 사용하므로 추가 DDL은 없다.

## 게시 절차

1. ADMIN이 시험, 회차, 과목을 생성한다.
2. PDF를 과목에 업로드한다. 추출 후보는 항상 `DRAFT` 및 `MISSING`으로 생성된다.
3. 원본 PDF와 문항 본문·보기를 대조하고 정답을 입력한 뒤 `VERIFIED`로 저장한다.
4. 문서 전체 게시를 실행한다. 하나라도 정답 미확인 또는 미검수 문항이면 서버가 거부한다.
5. 모든 과목에 게시·검수 완료 문항이 생긴 뒤 회차를 공개한다.
6. STUDENT 계정에서 `/public-exams` 노출과 응시 흐름을 확인한다.

스캔 이미지 PDF는 OCR을 수행하지 않는다. 텍스트 추출이 불가능하면 업로드가 422로 거부되며, OCR 처리된 PDF를 준비해야 한다.
