question_bank_system/
├── 📄 main.py                          # FastAPI 메인 애플리케이션
├── 📄 models.py                        # SQLAlchemy 데이터베이스 모델
├── 📄 config.py                        # 설정 파일
├── 📄 schema.sql                       # PostgreSQL 스키마
├── 📄 requirements.txt                 # Python 의존성
├── 📄 README.md                        # 프로젝트 소개
├── 📄 DEPLOYMENT.md                    # 배포 가이드
├── 📄 .env.example                     # 환경 변수 템플릿
│
├── 📁 routes/                          # API 라우트
│   ├── 📄 __init__.py
│   ├── 📄 questions.py                 # 문제 관련 엔드포인트
│   ├── 📄 files.py                     # 파일 업로드 엔드포인트
│   └── 📄 subjects.py                  # 과목 관리 엔드포인트
│
├── 📁 services/                        # 비즈니스 로직
│   ├── 📄 __init__.py
│   ├── 📄 excel_processor.py           # Excel 파일 처리
│   ├── 📄 file_processor.py            # 일반 파일 처리
│   ├── 📄 question_generator.py        # OpenAI API 통합
│   └── 📄 question_retriever.py        # 문제 검색 (선택사항)
│
├── 📁 schemas/                         # Pydantic 데이터 스키마
│   ├── 📄 __init__.py
│   └── 📄 questions.py                 # 문제 관련 스키마
│
├── 📁 uploads/                         # 업로드된 파일 저장 디렉토리
│   └── (파일 자동 생성)
│
└── 📁 frontend/                        # Next.js 프론트엔드
    ├── 📄 package.json                 # Node.js 의존성
    ├── 📄 tsconfig.json                # TypeScript 설정
    ├── 📄 next.config.js               # Next.js 설정
    ├── 📄 tailwind.config.js           # Tailwind CSS 설정
    ├── 📄 postcss.config.js            # PostCSS 설정
    ├── 📄 .env.local                   # 환경 변수 (개발)
    ├── 📄 SETUP.md                     # 프론트엔드 설정 가이드
    │
    ├── 📁 src/
    │   ├── 📁 pages/                   # 페이지 컴포넌트
    │   │   ├── 📄 index.tsx            # 메인 페이지 (홈)
    │   │   ├── 📄 upload.tsx           # 파일 업로드 페이지
    │   │   ├── 📄 quiz.tsx             # 문제 풀이 페이지
    │   │   └── 📄 manage.tsx           # 문제 관리 페이지 (선택사항)
    │   │
    │   ├── 📁 components/              # 재사용 가능한 컴포넌트
    │   │   ├── 📄 QuestionCard.tsx    # 문제 카드 컴포넌트
    │   │   ├── 📄 Header.tsx          # 헤더 컴포넌트
    │   │   └── 📄 Footer.tsx          # 푸터 컴포넌트
    │   │
    │   ├── 📁 lib/                     # 유틸리티 및 도우미
    │   │   ├── 📄 api.ts              # API 클라이언트
    │   │   └── 📄 types.ts            # TypeScript 타입 정의
    │   │
    │   └── 📄 globals.css              # 전역 CSS
    │
    └── 📁 public/                      # 정적 파일
        └── (이미지, 폰트 등)

═══════════════════════════════════════════════════════════════

📊 데이터베이스 스키마:

subjects (과목)
├── id: INTEGER PRIMARY KEY
├── name: VARCHAR(100) UNIQUE
├── description: TEXT
└── created_at: TIMESTAMP

questions (문제)
├── id: INTEGER PRIMARY KEY
├── subject_id: INTEGER FK
├── question_type: VARCHAR(20)
├── title: VARCHAR(255)
├── content: TEXT
├── correct_answer: TEXT
├── explanation: TEXT
├── difficulty: VARCHAR(20)
├── source_file: VARCHAR(255)
├── options: TEXT (JSON)
├── tags: TEXT
├── created_at: TIMESTAMP
└── updated_at: TIMESTAMP

excel_questions (Excel 기록)
├── id: INTEGER PRIMARY KEY
├── question_id: INTEGER FK
├── excel_row_number: INTEGER
└── file_name: VARCHAR(255)

code_files (코드 파일)
├── id: INTEGER PRIMARY KEY
├── file_name: VARCHAR(255)
├── file_path: VARCHAR(500)
├── file_type: VARCHAR(20)
├── file_content: TEXT
├── subject_id: INTEGER FK
└── uploaded_at: TIMESTAMP

user_progress (사용자 풀이 기록)
├── id: INTEGER PRIMARY KEY
├── user_id: VARCHAR(100)
├── question_id: INTEGER FK
├── is_correct: VARCHAR(20)
├── user_answer: TEXT
└── attempted_at: TIMESTAMP

═══════════════════════════════════════════════════════════════

🔌 API 엔드포인트 요약:

[과목]
GET    /api/subjects           # 모든 과목 조회
GET    /api/subjects/{id}      # 특정 과목 조회
POST   /api/subjects           # 과목 생성
PUT    /api/subjects/{id}      # 과목 수정
DELETE /api/subjects/{id}      # 과목 삭제

[문제]
GET    /api/questions          # 문제 목록 조회
GET    /api/questions/{id}     # 특정 문제 조회
POST   /api/questions          # 문제 생성
PUT    /api/questions/{id}     # 문제 수정
DELETE /api/questions/{id}     # 문제 삭제
POST   /api/questions/random/quiz    # 랜덤 문제 출제
GET    /api/questions/stats/difficulty  # 난이도별 통계

[파일]
POST   /api/files/upload/excel # Excel 파일 업로드
POST   /api/files/upload/code  # 코드 파일 업로드 (AI 문제 생성)
GET    /api/files/list         # 업로드된 파일 목록
DELETE /api/files/{id}         # 파일 삭제

═══════════════════════════════════════════════════════════════

🚀 빠른 시작:

1. Backend 시작:
   cd question_bank_system
   python -m venv venv
   venv\Scripts\activate
   pip install -r requirements.txt
   cp .env.example .env
   # .env 파일 수정 (DATABASE_URL, OPENAI_API_KEY)
   python main.py

2. Frontend 시작:
   cd frontend
   npm install
   npm run dev

3. 웹 브라우저 접속:
   Frontend: http://localhost:3000
   API: http://localhost:8000
   API 문서: http://localhost:8000/docs

═══════════════════════════════════════════════════════════════
