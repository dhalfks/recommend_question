# 문제 은행 시스템 (Question Bank System)

Excel 기반 및 AI를 활용한 코드 기반 문제 자동 생성 시스템입니다.

## 기술 스택

### Backend
- **Framework**: FastAPI (Python)
- **Database**: PostgreSQL (Neon/Supabase)
- **AI**: Google OpenAI API
- **File Processing**: openpyxl, pandas

### Frontend
- **Framework**: Next.js
- **Deployment**: Vercel
- **Styling**: Tailwind CSS (권장)

### Database
- **Primary**: PostgreSQL (Neon/Supabase)
- **ORM**: SQLAlchemy

## 주요 기능

### 1. Excel 기반 문제 관리
- Excel 파일 업로드
- 자동 파싱 및 데이터베이스 저장
- 난이도 및 과목별 분류

### 2. 코드 기반 문제 자동 생성
- 다양한 파일 형식 지원 (.java, .js, .sql, .txt, .md)
- OpenAI API를 사용한 AI 기반 문제 생성
- 정답 및 설명 자동 작성

### 3. 문제 출제 기능
- 난이도별 랜덤 문제 출제
- 과목별 필터링
- 다중 문제 동시 출제

### 4. 사용자 풀이 기록
- 문제 풀이 기록 저장
- 통계 및 분석

## 프로젝트 구조

```
question_bank_system/
├── main.py                      # FastAPI 메인 애플리케이션
├── models.py                    # SQLAlchemy 데이터베이스 모델
├── config.py                    # 설정 파일
├── requirements.txt             # Python 의존성
├── schema.sql                   # 데이터베이스 스키마
├── .env.example                 # 환경 변수 템플릿
├── routes/                      # API 라우트
│   ├── questions.py            # 문제 관련 엔드포인트
│   ├── files.py                # 파일 업로드 관련 엔드포인트
│   └── subjects.py             # 과목 관련 엔드포인트
├── services/                    # 비즈니스 로직
│   ├── excel_processor.py       # Excel 파일 처리
│   ├── file_processor.py        # 일반 파일 처리
│   ├── question_generator.py    # OpenAI API 통합
│   └── question_retriever.py    # 문제 검색 및 조회
├── schemas/                     # Pydantic 데이터 스키마
│   └── questions.py             # 문제 관련 스키마
├── uploads/                     # 업로드된 파일 저장 디렉토리
└── frontend/                    # Next.js 프론트엔드 (별도 폴더)
```

## 설치 및 실행

### Backend 설정

1. **Python 환경 설정**
```bash
cd question_bank_system
python -m venv venv

# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate
```

2. **의존성 설치**
```bash
pip install -r requirements.txt
```

3. **환경 변수 설정**
```bash
# .env 파일 생성 (Neon/Supabase 자격증명 추가)
cp .env.example .env
```

4. **데이터베이스 초기화**
```bash
# Neon/Supabase에서 schema.sql 실행
# 또는 Alembic migration 사용
```

5. **서버 실행**
```bash
python main.py
# 또는
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

서버는 `http://localhost:8000`에서 실행됩니다.

### API 문서
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

### Frontend 설정

1. **Next.js 프로젝트 생성**
```bash
npx create-next-app@latest frontend --typescript
cd frontend
```

2. **환경 변수 설정** (.env.local)
```
NEXT_PUBLIC_API_URL=http://localhost:8000/api
```

3. **필요한 패키지 설치**
```bash
npm install axios react-query tailwindcss
```

4. **개발 서버 실행**
```bash
npm run dev
```

## API 엔드포인트

### 과목 관리
- `GET /api/subjects` - 모든 과목 조회
- `GET /api/subjects/{id}` - 특정 과목 조회
- `POST /api/subjects` - 과목 생성
- `PUT /api/subjects/{id}` - 과목 수정
- `DELETE /api/subjects/{id}` - 과목 삭제

### 문제 관리
- `GET /api/questions` - 문제 목록 조회
- `GET /api/questions/{id}` - 특정 문제 조회
- `POST /api/questions` - 문제 생성
- `PUT /api/questions/{id}` - 문제 수정
- `DELETE /api/questions/{id}` - 문제 삭제
- `POST /api/questions/random/quiz` - 랜덤 문제 출제
- `GET /api/questions/stats/difficulty` - 난이도별 통계

### 파일 관리
- `POST /api/files/upload/excel` - Excel 파일 업로드
- `POST /api/files/upload/code` - 코드 파일 업로드
- `GET /api/files/list` - 업로드된 파일 목록
- `DELETE /api/files/{id}` - 파일 삭제

## Excel 파일 형식

| 열 | 필드 | 설명 | 필수 |
|----|------|------|------|
| A | 질문 제목 | 문제의 제목 | ✓ |
| B | 문제 내용 | 문제의 상세 내용 | ✓ |
| C | 난이도 | EASY, MEDIUM, HARD, EXPERT | ✓ |
| D | 정답 | 정답 내용 | |
| E | 설명 | 정답 설명 | |
| F | 선택지 | JSON 형식 | |
| G | 태그 | 쉼표로 구분 | |

## OpenAI API 설정

1. **API 키 획득**
   - [Google AI Studio](https://makersuite.google.com/app/apikey)에서 API 키 생성
   - `.env` 파일에 `OPENAI_API_KEY` 추가

2. **코드 파일 업로드 시 자동 문제 생성**
   - 지원 형식: .java, .js, .sql, .txt, .md
   - AI가 자동으로 객관식 문제 5개 생성
   - 정답 및 설명 포함

## 배포

### Backend (Railway/Render/Heroku)
```bash
# Dockerfile 생성 및 배포
```

### Frontend (Vercel)
```bash
npx vercel deploy
```

## 환경 변수 설명

| 변수명 | 설명 | 예시 |
|--------|------|------|
| DATABASE_URL | PostgreSQL 연결 문자열 | postgresql://user:pass@host/db |
| OPENAI_API_KEY | Google OpenAI API 키 | your_api_key |
| SERVER_HOST | 서버 호스트 | 0.0.0.0 |
| SERVER_PORT | 서버 포트 | 8000 |
| UPLOAD_DIR | 파일 업로드 디렉토리 | uploads |
| CORS_ORIGINS | CORS 허용 출처 | ["http://localhost:3000"] |

## 주의사항

- PostgreSQL 데이터베이스가 필요합니다 (Neon 또는 Supabase 권장)
- OpenAI API 키가 필요합니다 (코드 기반 문제 생성 시)
- 파일 업로드 크기 제한: 10MB (config.py에서 조정 가능)

## 라이센스

MIT

## 문제 해결

### 1. 데이터베이스 연결 오류
```
DatabaseError: could not translate host name
```
→ DATABASE_URL 확인 및 Neon/Supabase 네트워크 설정 확인

### 2. OpenAI API 오류
```
AuthError: Invalid API key
```
→ .env 파일에서 OPENAI_API_KEY 확인

### 3. Excel 파일 인코딩 오류
→ Excel 파일을 UTF-8로 저장

## 추가 개선 사항

- [ ] 사용자 인증 시스템 (JWT)
- [ ] 문제 카테고리 자동 분류
- [ ] 시험 모드 및 타이머
- [ ] 사용자별 통계 및 분석 대시보드
- [ ] 문제 난이도 자동 조정 (적응형 학습)
- [ ] 다국어 지원
