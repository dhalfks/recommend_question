# 문제 은행 시스템

FastAPI, Next.js, PostgreSQL을 사용하는 문제 출제·풀이·학습 분석 시스템입니다. Excel과 코드 파일로 문제를 등록하고, 학생별 풀이 기록을 바탕으로 대시보드와 맞춤 추천을 제공합니다.

## 주요 기능

- 학생·교수자·관리자 회원가입과 JWT 인증
- 과목, 소제목, 난이도별 랜덤 문제 출제
- Excel 일괄 등록 및 직접 문제 출제
- 코드 파일 기반 AI 문제 생성 및 코드 답안 채점
- 학생 풀이 기록, 점수, 성취도, 풀이 시간 저장
- 학생 대시보드와 교수자용 문항·학생 분석
- 유사 학습자 오답 단원, 개인 오답, 적응형 문제 추천

## 기술 구성

- Backend: FastAPI, SQLAlchemy, PostgreSQL
- Frontend: Next.js 14, React 18, TypeScript, Tailwind CSS, Axios
- Database: Neon PostgreSQL
- AI: OpenAI API
- Deployment: Vercel 단일 프로젝트

## 프로젝트 구조

```text
question_bank_system/
├── main.py
├── config.py
├── models.py
├── requirements.txt
├── vercel.json
├── schema.sql
├── routes/
│   ├── auth.py
│   ├── files.py
│   ├── progress.py
│   ├── questions.py
│   ├── recommendations.py
│   └── subjects.py
├── schemas/
│   ├── auth.py
│   ├── progress.py
│   └── questions.py
├── services/
│   ├── auth.py
│   ├── answer_enrichment.py
│   ├── excel_processor.py
│   ├── file_processor.py
│   ├── question_generator.py
│   └── recommendation.py
└── frontend/
    ├── package.json
    ├── next.config.js
    └── src/
        ├── components/
        ├── contexts/
        ├── lib/
        └── pages/
```

더 자세한 내용은 [프로젝트 구조 문서](docs/PROJECT_STRUCTURE.md)를 참고하세요.

## 로컬 실행

### 1. 백엔드

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
Copy-Item .env.example .env
```

`.env`에서 최소한 다음 값을 설정합니다.

```env
DATABASE_URL=postgresql://user:password@host/database?sslmode=require
JWT_SECRET_KEY=충분히-긴-무작위-문자열
OPENAI_API_KEY=sk-...
UPLOAD_DIR=uploads
CORS_ORIGINS=["http://localhost:3000"]
```

서버를 실행합니다.

```powershell
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

- API: `http://localhost:8000`
- Swagger: `http://localhost:8000/docs`
- Health check: `http://localhost:8000/health`

### 2. 프런트엔드

```powershell
Set-Location frontend
npm install
```

`frontend/.env.local`:

```env
NEXT_PUBLIC_API_URL=http://localhost:8000/api
```

```powershell
npm run dev
```

웹 화면은 `http://localhost:3000`에서 확인합니다.

## 환경변수

| 이름 | 용도 | 배포 권장값 |
|---|---|---|
| `DATABASE_URL` | PostgreSQL 연결 문자열 | Neon pooled connection string |
| `JWT_SECRET_KEY` | 로그인 토큰 서명 | 긴 무작위 문자열 |
| `JWT_ACCESS_TOKEN_EXPIRE_MINUTES` | 토큰 유효시간 | `480` |
| `ADMIN_SIGNUP_CODE` | 관리자 가입 코드 | 운영 전용 비밀값 |
| `OPENAI_API_KEY` | AI 문제 생성·채점 | OpenAI API 키 |
| `OPENAI_MODEL` | 사용할 OpenAI 모델 | 프로젝트 설정값 |
| `OPENAI_GRADING_MODEL` | 코드 1차 저비용 채점 모델 | `gpt-5.6-luna` |
| `OPENAI_GRADING_REVIEW_MODEL` | 애매한 코드의 2차 정밀 채점 모델 | `gpt-5.6-sol` |
| `OPENAI_GRADING_CONFIDENCE_THRESHOLD` | 2차 채점으로 전환할 최소 확신도 | `0.75` |
| `UPLOAD_DIR` | 임시 업로드 위치 | Vercel에서는 `/tmp/uploads` |
| `CORS_ORIGINS` | 허용할 프런트 출처 | JSON 배열 |
| `NEXT_PUBLIC_API_URL` | 브라우저의 API 기본 경로 | 통합 Vercel 배포에서는 `/api` |

환경변수와 비밀키가 들어 있는 `.env` 및 `.env.local`은 Git에 커밋하지 않습니다.

## 주요 API

모든 보호 API는 로그인으로 발급받은 Bearer 토큰이 필요합니다.

### 인증

- `POST /api/auth/register`
- `POST /api/auth/login`
- `GET /api/auth/me`
- `PUT /api/auth/me`

### 과목 및 문제

- `GET /api/subjects`
- `POST /api/subjects`
- `GET /api/questions`
- `POST /api/questions`
- `GET /api/questions/subject-units`
- `POST /api/questions/random/quiz`

### 풀이 및 분석

- `POST /api/progress/submit`
- `GET /api/progress/dashboard`
- `GET /api/progress/question-analytics`
- `GET /api/progress/student-analytics`

### 추천

- `GET /api/recommendations/quiz`
- `GET /api/recommendations/peer-missed`
- `GET /api/recommendations/peer-missed-units`
- `GET /api/recommendations/my-wrong`

### 파일

- `GET /api/files/template/excel`
- `POST /api/files/upload/excel`
- `POST /api/files/upload/code`
- `GET /api/files/list`
- `DELETE /api/files/{id}`

전체 요청과 응답 형식은 `/docs`의 Swagger UI에서 확인할 수 있습니다.

## Vercel 배포

현재 저장소는 루트 `vercel.json`을 통해 FastAPI와 Next.js를 한 Vercel 프로젝트에 함께 배포합니다.

1. GitHub 저장소를 Vercel 프로젝트에 연결합니다.
2. Root Directory는 저장소 루트로 둡니다.
3. Output Directory override는 사용하지 않습니다.
4. 다음 환경변수를 Vercel 프로젝트에 설정합니다.

```env
NEXT_PUBLIC_API_URL=/api
DATABASE_URL=postgresql://...
JWT_SECRET_KEY=...
OPENAI_API_KEY=sk-...
UPLOAD_DIR=/tmp/uploads
```

5. 새 커밋을 푸시하거나 캐시 없이 Redeploy합니다.

상세 절차는 [배포 가이드](docs/DEPLOYMENT.md)를 참고하세요.

## 문제 해결

### 대시보드는 열리지만 일부 카드가 비어 있음

브라우저 개발자 도구의 Network 탭에서 다음 요청을 각각 확인합니다.

```text
/api/progress/dashboard
/api/subjects
/api/recommendations/peer-missed-units
/api/recommendations/my-wrong
```

`401`은 토큰, `403`은 역할, `500`은 백엔드 또는 DB, 약 10초 후 canceled는 클라이언트 시간 초과를 의미합니다.

### 과목 또는 문제 등록이 리다이렉트됨

목록·등록 경로는 끝 슬래시 없이 호출합니다.

```text
/api/subjects
/api/questions
```

### Neon Tables 화면에 일부 행만 보임

Tables 화면은 페이지 단위로 표시합니다. 실제 개수는 SQL Editor에서 확인합니다.

```sql
SELECT COUNT(*) AS question_count, MIN(id), MAX(id)
FROM questions;
```

수동 import 후 새 ID가 충돌하면 시퀀스를 현재 최대 ID에 맞춥니다.

```sql
SELECT setval(
    pg_get_serial_sequence('questions', 'id'),
    COALESCE(MAX(id), 1),
    MAX(id) IS NOT NULL
)
FROM questions;
```
