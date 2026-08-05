# 통합 Vercel 배포 가이드

이 프로젝트는 하나의 GitHub 저장소와 하나의 Vercel 프로젝트에서 Next.js 프런트엔드와 FastAPI 백엔드를 함께 배포합니다. 데이터는 Neon PostgreSQL에 저장합니다.

## 배포 구조

```text
브라우저
  ├─ /, /login, /quiz ... → Next.js
  └─ /api/*, /docs        → FastAPI
                              ├─ Neon PostgreSQL
                              └─ OpenAI API
```

루트 `vercel.json`이 다음 빌드를 담당합니다.

- `main.py`: `@vercel/python`
- `frontend/package.json`: `@vercel/next`
- `/api/*`: FastAPI로 전달
- 나머지 경로: Next.js로 전달

## 1. 배포 전 확인

### 백엔드

```powershell
.venv\Scripts\python.exe -m py_compile main.py config.py models.py
.venv\Scripts\python.exe -c "import main; print(type(main.app).__name__)"
```

로컬 실행:

```powershell
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### 프런트엔드

```powershell
Set-Location frontend
npm install
npx tsc --noEmit
npm run build
```

## 2. Neon 준비

Neon에서 프로젝트와 데이터베이스를 만든 후 pooled connection string을 준비합니다.

```env
DATABASE_URL=postgresql://user:password@host/database?sslmode=require
```

SQL Editor에서 기본 상태를 확인합니다.

```sql
SELECT current_database(), current_user;

SELECT table_name
FROM information_schema.tables
WHERE table_schema = 'public'
ORDER BY table_name;
```

주요 테이블:

```text
users
subjects
questions
excel_questions
code_files
user_progress
quiz_sessions
```

## 3. Vercel 프로젝트 생성

1. Vercel에서 GitHub 저장소를 Import합니다.
2. Root Directory는 비워 두어 저장소 루트를 사용합니다.
3. 루트 `vercel.json`이 빌드를 제어하므로 프런트만 가리키는 `frontend` Root Directory를 사용하지 않습니다.
4. Output Directory override는 끕니다.
5. 배포 브랜치를 `main`으로 설정합니다.

정상 빌드는 Python 함수와 Next.js 출력물을 모두 생성해야 합니다. 수십 밀리초 만에 `no files were prepared`로 끝나면 빈 배포이므로 Root Directory와 `vercel.json` 인식을 다시 확인합니다.

## 4. Vercel 환경변수

같은 Vercel 프로젝트에 프런트와 백엔드 변수를 모두 설정합니다.

```env
NEXT_PUBLIC_API_URL=/api
DATABASE_URL=postgresql://...
JWT_SECRET_KEY=충분히-긴-무작위-문자열
JWT_ACCESS_TOKEN_EXPIRE_MINUTES=480
OPENAI_API_KEY=sk-...
OPENAI_MODEL=gpt-5.6-sol
UPLOAD_DIR=/tmp/uploads
CORS_ORIGINS=["https://실제도메인.vercel.app"]
```

선택 항목:

```env
ADMIN_SIGNUP_CODE=관리자-가입-코드
MAX_FILE_SIZE=10485760
```

주의사항:

- 키 이름은 `OPEN_API_KEY`가 아니라 `OPENAI_API_KEY`입니다.
- `NEXT_PUBLIC_API_URL`은 빌드 시 번들에 반영되므로 변경 후 재배포해야 합니다.
- 통합 배포에서는 `/api`를 사용합니다.
- Vercel 서버리스 파일 시스템은 영구 저장소가 아니며 쓰기 작업은 `/tmp`만 사용합니다.
- `.env` 파일을 Git에 커밋하지 않습니다.

## 5. 배포 및 확인

```powershell
git status
git add <변경한 파일>
git commit -m "describe deployment change"
git push origin main
```

Vercel 배포가 끝나면 다음을 확인합니다.

```text
https://도메인.vercel.app/
https://도메인.vercel.app/docs
https://도메인.vercel.app/openapi.json
```

`/docs`에서 다음 순서로 API를 검증합니다.

1. `POST /api/auth/login`
2. 응답의 `access_token` 복사
3. Swagger의 Authorize에 토큰 입력
4. `GET /api/auth/me`
5. `GET /api/subjects`
6. `GET /api/progress/dashboard`
7. `GET /api/recommendations/peer-missed-units`

## 6. 브라우저 검증

개발자 도구의 Network 탭에서 요청 URL, 최종 Status, Response를 확인합니다.

| 상태 | 의미 | 확인할 부분 |
|---|---|---|
| `200` | 정상 | 응답 데이터 구조 |
| `307`, `308` | 리다이렉트 | trailing slash, 도메인 정규화 |
| `401` | 인증 실패 | access token |
| `403` | 권한 실패 | 사용자 role |
| `404` | 라우팅 실패 | `vercel.json`, API 경로 |
| `422` | 입력 검증 실패 | 요청 JSON |
| `500` | 서버 오류 | Vercel Runtime Logs, DB 스키마 |
| `canceled` 약 10초 | Axios 시간 초과 | 느린 DB·추천 쿼리 |

과목과 문제 목록·등록 API는 끝 슬래시 없이 사용합니다.

```text
GET  /api/subjects
POST /api/subjects
GET  /api/questions
POST /api/questions
```

## 7. 데이터베이스 점검

### 문제 개수

```sql
SELECT COUNT(*) AS question_count, MIN(id), MAX(id)
FROM questions;
```

Neon Tables 화면은 일부 페이지만 보여줄 수 있으므로 전체 개수는 SQL 결과를 기준으로 판단합니다.

### 시퀀스

수동으로 ID를 지정해 import한 뒤 등록이 실패하면 확인합니다.

```sql
SELECT last_value, is_called
FROM questions_id_seq;
```

복구:

```sql
SELECT setval(
    pg_get_serial_sequence('questions', 'id'),
    COALESCE(MAX(id), 1),
    MAX(id) IS NOT NULL
)
FROM questions;
```

### 풀이 기록 연결

```sql
SELECT
    u.id,
    u.email,
    u.role,
    COUNT(up.id) AS attempts
FROM users u
LEFT JOIN user_progress up ON up.user_id = u.id::text
GROUP BY u.id, u.email, u.role
ORDER BY u.id;
```

현재 `user_progress.user_id`는 문자열이고 `users.id`는 정수입니다. 애플리케이션은 문자열 변환으로 연결합니다. 타입과 코드를 함께 마이그레이션하지 않은 상태에서 외래키만 추가하면 안 됩니다.

## 8. 대시보드 및 추천 문제 해결

학생 메인 화면은 다음 요청을 사용합니다.

```text
/api/progress/dashboard
/api/subjects
/api/recommendations/peer-missed-units
/api/recommendations/my-wrong
```

기본 대시보드와 부가 추천 요청은 독립적으로 처리됩니다. 추천 API가 실패하더라도 풀이 현황과 과목 목록은 표시되어야 합니다.

`peer-missed-units`가 느리면 다음을 확인합니다.

- 사용자·문제별 최신 풀이만 조회하는지
- 문제별 반복 조회가 없는지
- `user_progress.user_id`, `question_id` 인덱스가 있는지
- Neon과 Vercel Runtime Logs의 쿼리 시간을 확인했는지

## 9. 재배포

환경변수나 빌드 설정을 변경한 경우 Vercel Deployments에서 캐시 없이 Redeploy합니다. 코드 변경은 `main` 브랜치에 푸시하면 자동 배포됩니다.

배포 후 이전 JavaScript가 남아 있으면 브라우저에서 강력 새로고침합니다.

```text
Windows: Ctrl + Shift + R
macOS: Command + Shift + R
```
