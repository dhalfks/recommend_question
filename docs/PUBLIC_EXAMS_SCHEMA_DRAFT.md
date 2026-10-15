# 공통 기출 스키마 조사 및 마이그레이션 초안

작성일: 2026-10-15

## 실행 여부

- 운영 DB 변경 SQL은 실행하지 않았다.
- `INSERT`, `UPDATE`, `DELETE`, `CREATE`, `ALTER`, `DROP`은 어떤 DB에도 실행하지 않았다.
- 메타데이터 조회는 `BEGIN TRANSACTION READ ONLY` 안에서 수행하고 `ROLLBACK`했다.
- 애플리케이션 코드는 수정하지 않았다.

## DB 연결 방식

- `config.py`의 Pydantic Settings가 `.env`의 `DATABASE_URL`을 읽는다.
- `models.py`가 이 값을 SQLAlchemy `create_engine()`에 전달한다.
- 드라이버는 `psycopg2-binary`이며 애플리케이션 시작 시 `create_tables()`가 호출된다.
- Alembic은 사용하지 않고 `migrations/`의 SQL을 수동 관리한다.

## 실제 확인한 DB

현재 작업 공간의 `.env`에 설정된 DB에 읽기 전용으로 접속해 확인했다.

- PostgreSQL 18.1, Windows 빌드
- 데이터베이스: `question_bank`
- 스키마: `public`
- 확인된 테이블: `users`, `subjects`, `questions`, `excel_questions`,
  `code_files`, `user_progress`, `quiz_sessions`

서버가 Windows PostgreSQL로 식별되므로 이 연결은 Neon 운영 DB가 아니라 로컬 DB다.
운영 Vercel/Neon의 환경 변수는 저장소에서 확인할 수 없으므로 운영 Neon 실제 스키마는
아직 확인되지 않았다. 접속 문자열이나 비밀번호는 출력하거나 문서에 기록하지 않았다.

## 소스 정의와 현재 연결 DB의 주요 차이

| 항목 | 소스/마이그레이션 기대값 | 현재 연결 DB | 확인 결과 |
|---|---|---|---|
| `users.professor_id` 및 소속 필드 | 존재 | 없음 | 불일치 |
| 학생-강사 체크 및 교수 검증 트리거 | 존재 기대 | 없음 | 불일치 |
| `questions.professor_id` | 존재 | 없음 | 불일치 |
| `questions.answer_type` | 존재 | 없음 | 불일치 |
| `code_files.professor_id` | 존재 | 없음 | 불일치 |
| `user_progress` 시간/세션 필드 | 존재 | 존재 | 일치 |
| `user_progress.user_id` FK | 없음 | 없음 | 일치하지만 무결성 위험 |
| 교수 소유권 관련 인덱스 | 존재 기대 | 없음 | 불일치 |
| `quiz_sessions.started_at/submitted_at/status` | 없음 | 없음 | 공통 기출에는 별도 설계 필요 |
| 문제 정답 필드 | nullable | nullable | 미확인 정답 표현 가능 |

현재 로컬 DB는 `models.py`를 최신 코드로 실행하면 시작 시 스키마 오류가 발생할 가능성이
있다. `create_tables()`는 `questions.answer_type` 등을 일부 보완하지만 교수 소유권 필드는
자동 보완하지 않는다.

## 운영 Neon에서 재확인할 점검표

- [ ] 연결 대상이 실제 운영 Neon 프로젝트/브랜치인지 확인
- [ ] 7개 기존 테이블의 존재와 스키마명 확인
- [ ] 모든 컬럼의 타입, null 허용, 기본값 비교
- [ ] `users.professor_id`, `questions.professor_id`, `code_files.professor_id` 확인
- [ ] `questions.answer_type`, `answer_code_snippet`, `is_required` 확인
- [ ] 학생-강사 체크 제약 및 교수 검증 트리거 확인
- [ ] 모든 외래키의 `ON DELETE` 정책 확인
- [ ] 교수 소유권, 진행 기록, 세션 관련 인덱스 확인
- [ ] SQLAlchemy enum 타입과 값 확인
- [ ] 공통 기출 테이블 이름 충돌 여부 확인
- [ ] 사용 DB 역할이 마이그레이션 DDL 권한을 갖는지 별도 확인

`readonly_schema_inspection.sql`은 위 항목 중 테이블, 컬럼, 기본값, 키, 체크 제약,
인덱스, enum과 사용자 정의 트리거를 변경 없이 확인한다.

## 초안 설계 범위

기존 강사 문제와 통계를 오염시키지 않도록 공통 기출은 별도 테이블로 분리했다.

- 시험 → 회차 → 실제 과목 → 문제의 계층
- PDF 원본 및 출처 메타데이터
- 학생별 응시와 문항별 저장 답안
- 서버 시각 기준 시작·마지막 활동·제출·포기 시각
- 문항별 소요 시간과 전체 소요 시간의 분리
- 미확인 정답의 `MISSING` 상태 및 게시 방지 제약

`total_elapsed_seconds`는 최종 제출 트랜잭션에서 DB 시각의
`submitted_at - started_at`으로 계산해 저장하는 것을 전제로 한다. 중단 후 재개해도 최초
`started_at`을 유지하므로 중단 시간은 전체 소요 시간에 포함된다. 문항별 시간은 별도
활동 시간이며 전체 시간과 같다고 가정하지 않는다.

UUID 응시 ID는 애플리케이션에서 생성해 전달하는 전제다. 따라서 `pgcrypto` 같은 확장이나
DB 함수 생성이 필요 없다.

## 기존 기능 영향

- 기존 테이블을 변경하지 않으므로 강사별 문제 접근 제어에는 직접 영향이 없다.
- 공통 응시는 기존 `user_progress`와 `quiz_sessions`에 기록하지 않아 추천과 대시보드에
  자동으로 섞이지 않는다.
- 기존 채점 함수는 추후 공통 서비스로 추출하거나 얇은 어댑터로 재사용할 수 있지만,
  이번 SQL은 애플리케이션 채점 흐름을 바꾸지 않는다.
- 기존 문항 타이머와 기존 `quiz_sessions.total_seconds`는 변경하지 않는다.
- 공통 기출 결과를 기존 대시보드에 포함하려면 출처가 분리된 별도 집계 API가 필요하다.
- 원본 PDF 본체는 Vercel 임시 파일시스템이 아니라 영구 객체 저장소에 두고,
  `storage_key`와 출처 정보만 DB에 저장해야 한다.

## 승인 전에 결정할 사항

1. 운영 Neon 읽기 전용 결과와 초안의 테이블/타입 충돌 여부
2. 객관식 외에 단답형을 초기 범위에 포함할지 여부
3. 정답 미확인 문항을 게시 금지할지, 풀이 가능하지만 채점 제외할지 여부
4. 중단 시간을 전체 소요 시간에 포함하는 정책
5. 한 학생의 동일 과목 동시 진행 응시를 허용할지 여부
6. PDF 영구 저장소와 `storage_key` 형식
7. 롤백 시 데이터 삭제 위험과 백업 절차
