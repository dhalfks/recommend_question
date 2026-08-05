# 프로젝트 구조

## 디렉터리

```text
question_bank_system/
├── main.py                         # FastAPI 앱, CORS, 라우터 등록
├── config.py                       # 환경변수 기반 설정
├── models.py                       # SQLAlchemy 모델과 DB 세션
├── requirements.txt                # Python 의존성
├── vercel.json                     # FastAPI + Next.js 통합 배포
├── schema.sql                      # PostgreSQL 초기 스키마
├── question_excel.py               # 문제 Excel 생성·가공
├── import_sample_excel.py          # 샘플 Excel import
├── init_local_db.py                # 로컬 DB 초기화
├── seed_adaptive_learning.py       # 적응형 학습 샘플 데이터
├── routes/
│   ├── auth.py                     # 가입, 로그인, 내 정보
│   ├── files.py                    # Excel·코드 파일 처리
│   ├── progress.py                 # 답안 제출, 대시보드, 분석
│   ├── questions.py                # 문제 CRUD와 랜덤 출제
│   ├── recommendations.py          # 추천 API
│   └── subjects.py                 # 과목 CRUD
├── schemas/
│   ├── auth.py                     # 인증 요청·응답 모델
│   ├── progress.py                 # 풀이 제출 모델
│   └── questions.py                # 과목·문제 모델
├── services/
│   ├── auth.py                     # 비밀번호 해시와 JWT
│   ├── answer_enrichment.py        # AI 답안 보강·채점
│   ├── excel_processor.py          # Excel 문제 import
│   ├── file_processor.py           # 업로드 파일 저장·읽기
│   ├── question_generator.py       # OpenAI 문제 생성
│   └── recommendation.py           # 유사 학습자·적응형 추천
├── uploads/                        # 로컬 업로드 디렉터리
└── frontend/
    ├── package.json
    ├── next.config.js
    ├── tsconfig.json
    ├── tailwind.config.js
    └── src/
        ├── globals.css
        ├── components/
        │   ├── CodeBlock.tsx
        │   ├── Footer.tsx
        │   ├── Navbar.tsx
        │   ├── ProtectedPage.tsx
        │   └── StudentDashboard.tsx
        ├── contexts/
        │   └── AuthContext.tsx
        ├── lib/
        │   └── api.ts
        └── pages/
            ├── _app.tsx
            ├── index.tsx
            ├── analytics.tsx
            ├── create-question.tsx
            ├── login.tsx
            ├── profile.tsx
            ├── quiz.tsx
            ├── register.tsx
            └── upload.tsx
```

`.env`, `.env.local`, 가상환경, `node_modules`, 빌드 결과물은 소스 구조에서 제외하며 Git에 커밋하지 않습니다.

## 요청 흐름

```text
Next.js page
  → frontend/src/lib/api.ts
    → /api/*
      → main.py
        → routes/*
          → services/*
            → SQLAlchemy
              → Neon PostgreSQL
```

인증된 요청에는 브라우저 `localStorage`의 `access_token`이 Bearer 토큰으로 추가됩니다.

## 데이터베이스 모델

### users

| 컬럼 | 타입 | 설명 |
|---|---|---|
| `id` | INTEGER PK | 사용자 ID |
| `name` | VARCHAR(100) | 이름 |
| `phone` | VARCHAR(30) | 전화번호 |
| `email` | VARCHAR(255) UNIQUE | 로그인 이메일 |
| `password_hash` | VARCHAR(512) | PBKDF2 비밀번호 해시 |
| `role` | ENUM | `STUDENT`, `PROFESSOR`, `ADMIN` |
| `created_at` | TIMESTAMP | 가입 시각 |

### subjects

| 컬럼 | 타입 | 설명 |
|---|---|---|
| `id` | INTEGER PK | 과목 ID |
| `name` | VARCHAR(100) UNIQUE | 과목명 |
| `description` | TEXT | 설명 |
| `created_at` | TIMESTAMP | 생성 시각 |

### questions

주요 컬럼:

```text
id, subject_id, question_type, title, content,
correct_answer, explanation, difficulty, source_file,
options, tags, external_id, subject_code, subject_unit,
code_snippet, answer_code_snippet, benchmark_time,
correct_option, is_required, created_at, updated_at
```

관계:

```text
questions.subject_id → subjects.id
```

### user_progress

학생이 문제별로 제출한 모든 시도를 저장합니다.

```text
id, user_id, question_id, is_correct, user_answer,
session_id, sequence_number, elapsed_seconds,
achievement_score, attempted_at
```

관계:

```text
user_progress.question_id → questions.id
```

현재 `user_id`는 `VARCHAR(100)`이며 애플리케이션에서 `users.id`를 문자열로 저장합니다. `users.id`와의 DB 외래키는 아직 없습니다.

### quiz_sessions

한 번의 문제 풀이 세션 요약을 저장합니다.

```text
id, user_id, total_seconds, total_questions,
correct_answers, score_percent, achievement_score, completed_at
```

관계:

```text
quiz_sessions.user_id → users.id
```

### 기타

- `excel_questions`: Excel 원본 행과 문제 연결
- `code_files`: 업로드한 코드 파일과 과목 연결

## API 구조

### 인증

```text
POST /api/auth/register
POST /api/auth/login
GET  /api/auth/me
PUT  /api/auth/me
```

### 과목

```text
GET    /api/subjects
POST   /api/subjects
GET    /api/subjects/{subject_id}
PUT    /api/subjects/{subject_id}
DELETE /api/subjects/{subject_id}
```

교수자·관리자만 과목을 생성·수정할 수 있고 관리자는 삭제할 수 있습니다.

### 문제

```text
GET    /api/questions
POST   /api/questions
GET    /api/questions/subject-units
GET    /api/questions/{question_id}
PUT    /api/questions/{question_id}
DELETE /api/questions/{question_id}
POST   /api/questions/random/quiz
GET    /api/questions/stats/difficulty
POST   /api/questions/admin/backfill-answers
```

목록·등록 URL은 Vercel 리다이렉트 충돌을 피하기 위해 끝 슬래시 없이 사용합니다.

### 풀이 및 분석

```text
POST /api/progress/submit
GET  /api/progress/dashboard
GET  /api/progress/question-analytics
GET  /api/progress/question-analytics/{question_id}
GET  /api/progress/student-analytics
GET  /api/progress/student-analytics/{student_id}
```

학생은 자신의 대시보드를 조회하고, 교수자·관리자는 문항 및 학생 분석을 조회합니다.

### 추천

```text
GET /api/recommendations/quiz
GET /api/recommendations/peer-missed
GET /api/recommendations/peer-missed-units
GET /api/recommendations/my-wrong
```

추천 서비스는 사용자·문제별 최신 풀이 기록을 DB에서 선별하고, 문제와 과목을 묶어 조회하여 반복 쿼리를 줄입니다.

### 파일

```text
GET    /api/files/template/excel
POST   /api/files/upload/excel
POST   /api/files/upload/code
GET    /api/files/list
DELETE /api/files/{file_id}
```

## 학생 대시보드 데이터 흐름

학생 메인 화면은 요청을 독립적으로 실행합니다.

```text
/api/progress/dashboard                 기본 학습 통계
/api/subjects                           출제 과목
/api/recommendations/peer-missed-units  유사 학생 오답 단원
/api/recommendations/my-wrong           내 최근 오답
```

추천 API가 실패해도 기본 대시보드와 과목 목록은 표시됩니다. 과목 선택 후 소제목은 다음 요청으로 불러옵니다.

```text
GET /api/questions/subject-units?subject_id={id}
```

난이도는 `EASY`, `MEDIUM`, `HARD`, `EXPERT` 네 단계입니다.

## 실행과 배포

로컬 백엔드:

```powershell
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

로컬 프런트:

```powershell
Set-Location frontend
npm run dev
```

운영 환경은 루트 `vercel.json`으로 FastAPI와 Next.js를 한 Vercel 프로젝트에 배포하며 Neon PostgreSQL을 사용합니다. 자세한 절차는 [DEPLOYMENT.md](DEPLOYMENT.md)를 참고하세요.
