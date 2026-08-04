# 문제 은행 시스템 - 설정 및 배포 가이드

## 빠른 시작

### 1. Backend 설정 (FastAPI)

#### 1.1 Python 환경 설정
```bash
# Python 3.10 이상 필요
python --version

# 가상 환경 생성
python -m venv venv

# 환경 활성화 (Windows)
venv\Scripts\activate

# 환경 활성화 (macOS/Linux)
source venv/bin/activate
```

#### 1.2 의존성 설치
```bash
pip install -r requirements.txt
```

#### 1.3 환경 변수 설정
```bash
# .env 파일 생성
cp .env.example .env

# .env 파일 편집 (데이터베이스, API 키 등)
# DATABASE_URL: Neon/Supabase PostgreSQL 연결 문자열
# OPENAI_API_KEY: Google OpenAI API 키
```

#### 1.4 데이터베이스 설정
- **Neon 설정** (권장):
  1. [Neon Console](https://console.neon.tech/)에 회원가입
  2. 새 프로젝트 생성
  3. 연결 문자열 복사
  4. `.env` 파일에 `DATABASE_URL`로 설정

- **Supabase 설정**:
  1. [Supabase](https://supabase.com/)에 회원가입
  2. 새 프로젝트 생성
  3. Connection String (psycopg2) 복사
  4. `.env` 파일에 `DATABASE_URL`로 설정

#### 1.5 데이터베이스 스키마 생성
```bash
# pgAdmin 또는 psql 클라이언트로 schema.sql 실행
psql -U your_user -d your_database -f schema.sql

# 또는 Neon/Supabase 웹 에디터에서 schema.sql 내용 복사/실행
```

#### 1.6 서버 실행
```bash
# 방법 1: Python 직접 실행
python main.py

# 방법 2: Uvicorn 서버
uvicorn main:app --reload --host 0.0.0.0 --port 8000

# 방법 3: 프로덕션 배포
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4
```

**서버 확인**:
- API: http://localhost:8000
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

### 2. Frontend 설정 (Next.js)

#### 2.1 프로젝트 초기화
```bash
cd frontend

# 의존성 설치
npm install
# 또는
yarn install
```

#### 2.2 환경 변수 설정
```bash
# .env.local 파일 확인/수정
NEXT_PUBLIC_API_URL=http://localhost:8000/api
```

#### 2.3 개발 서버 실행
```bash
npm run dev
```

**프론트엔드 확인**:
- http://localhost:3000

### 3. OpenAI API 설정

#### 3.1 API 키 획득
1. [Google AI Studio](https://makersuite.google.com/app/apikey) 접속
2. "Get API key" 클릭
3. "Create API key in new project" 또는 기존 프로젝트 선택
4. API 키 복사

#### 3.2 .env 파일에 설정
```
OPENAI_API_KEY=your_gemini_api_key_here
```

#### 3.3 테스트
```bash
# 코드 파일 업로드 시 자동으로 OpenAI API가 호출됨
# /api/files/upload/code 엔드포인트 사용
```

## API 사용 예제

### 1. 과목 생성
```bash
curl -X POST http://localhost:8000/api/subjects \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Python 기초",
    "description": "Python 프로그래밍 기초"
  }'
```

### 2. Excel 파일 업로드
```bash
curl -X POST http://localhost:8000/api/files/upload/excel \
  -F "file=@questions.xlsx" \
  -F "subject_id=1"
```

### 3. 코드 파일 업로드 (자동 문제 생성)
```bash
curl -X POST http://localhost:8000/api/files/upload/code \
  -F "file=@sample.java" \
  -F "subject_id=1" \
  -F "auto_generate=true"
```

### 4. 랜덤 문제 출제
```bash
curl -X POST http://localhost:8000/api/questions/random/quiz \
  -H "Content-Type: application/json" \
  -d '{
    "subject_id": 1,
    "difficulty": "MEDIUM",
    "count": 5
  }'
```

## 배포 가이드

### Backend 배포 (Railway/Render/Heroku)

#### Railway 배포
1. [Railway](https://railway.app/)에 회원가입
2. GitHub 저장소 연결
3. `main.py` 파일이 있는 디렉토리 선택
4. 환경 변수 설정 (DATABASE_URL, OPENAI_API_KEY)
5. 자동 배포

#### Heroku 배포 (기존)
```bash
# Procfile 생성
echo "web: uvicorn main:app --host 0.0.0.0 --port \$PORT" > Procfile

# Heroku 로그인
heroku login

# 앱 생성 및 배포
heroku create your-app-name
git push heroku main
```

### Frontend 배포 (Vercel)

#### Vercel 배포 (권장)
1. [Vercel](https://vercel.com/)에 회원가입
2. GitHub 저장소 연결
3. `frontend` 디렉토리 선택
4. 환경 변수 설정:
   ```
   NEXT_PUBLIC_API_URL=https://your-backend-api.com/api
   ```
5. 자동 배포

#### Next.js 빌드 및 실행
```bash
# 프로덕션 빌드
npm run build

# 프로덕션 서버 실행
npm start
```

## 시스템 아키텍처

```
┌─────────────────────────────────────────────────────┐
│                Frontend (Next.js)                    │
│              Hosted on Vercel                        │
│  (http://yourapp.vercel.app)                         │
└────────────────┬────────────────────────────────────┘
                 │
                 │ HTTP/REST API
                 │
┌────────────────▼────────────────────────────────────┐
│             Backend (FastAPI)                        │
│         Hosted on Railway/Render                     │
│   (https://your-backend-api.railway.app)             │
├──────────────────────────────────────────────────────┤
│  • File Upload & Processing                         │
│  • OpenAI API Integration                           │
│  • Question Management                              │
│  • Random Question Generation                       │
└────────────────┬────────────────────────────────────┘
                 │
        ┌────────┴────────┐
        │                 │
┌───────▼────────┐  ┌─────▼──────────┐
│  PostgreSQL    │  │  OpenAI API    │
│  (Neon/Supabase)  │  (AI Questions)  │
└────────────────┘  └────────────────┘
```

## 주요 파일 설명

### Backend
- `main.py`: FastAPI 메인 애플리케이션
- `models.py`: SQLAlchemy 데이터베이스 모델
- `config.py`: 애플리케이션 설정
- `routes/`: API 엔드포인트
  - `questions.py`: 문제 관련 API
  - `files.py`: 파일 업로드 API
  - `subjects.py`: 과목 관리 API
- `services/`: 비즈니스 로직
  - `excel_processor.py`: Excel 파일 처리
  - `question_generator.py`: OpenAI API 통합
  - `file_processor.py`: 일반 파일 처리
- `schema.sql`: 데이터베이스 스키마

### Frontend
- `src/pages/`: 페이지 컴포넌트
  - `index.tsx`: 메인 페이지
  - `upload.tsx`: 파일 업로드 페이지
  - `quiz.tsx`: 문제 풀이 페이지
- `src/lib/`: 유틸리티
  - `api.ts`: API 클라이언트
- `tailwind.config.js`: Tailwind CSS 설정
- `.env.local`: 환경 변수

## 환경 변수 참고값

```env
# 데이터베이스
DATABASE_URL=postgresql://user:password@host:5432/database

# OpenAI API
OPENAI_API_KEY=AIzaSyB...

# 서버 설정
SERVER_HOST=0.0.0.0
SERVER_PORT=8000

# 파일 업로드
UPLOAD_DIR=uploads
MAX_FILE_SIZE=10485760

# CORS
CORS_ORIGINS=["http://localhost:3000", "https://yourapp.vercel.app"]
```

## 문제 해결

### 1. 데이터베이스 연결 오류
**증상**: `could not translate host name`
**해결**:
- Neon/Supabase 연결 문자열 확인
- 방화벽 설정 확인
- 데이터베이스 사용자명/비밀번호 확인

### 2. OpenAI API 오류
**증상**: `Invalid API key`
**해결**:
- API 키 확인
- API 활성화 확인
- 배포 환경에서 환경 변수 설정 확인

### 3. CORS 오류
**증상**: `Access-Control-Allow-Origin` 오류
**해결**:
- `config.py`의 `CORS_ORIGINS` 확인
- 프론트엔드 URL 추가

### 4. Excel 파일 인코딩 오류
**증상**: 한글 문자 깨짐
**해결**:
- Excel 파일을 UTF-8로 저장

### 5. 파일 업로드 오류
**증상**: `413 Payload Too Large`
**해결**:
- `config.py`의 `MAX_FILE_SIZE` 증가
- 파일 크기 확인

## 참고 자료

- [FastAPI 공식 문서](https://fastapi.tiangolo.com/)
- [Next.js 공식 문서](https://nextjs.org/docs)
- [SQLAlchemy 공식 문서](https://docs.sqlalchemy.org/)
- [Google OpenAI API](https://ai.google.dev/)
- [Neon PostgreSQL](https://neon.tech/)
- [Supabase](https://supabase.com/)
- [Vercel](https://vercel.com/)
- [Railway](https://railway.app/)

## 추가 기능 (향후 개발)

- [ ] 사용자 인증 (JWT)
- [ ] 사용자별 학습 통계
- [ ] 문제 난이도 자동 조정
- [ ] 시험 모드
- [ ] 팀 협업 기능
- [ ] 모바일 앱
- [ ] 다국어 지원
- [ ] 문제 기여 커뮤니티
