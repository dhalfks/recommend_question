# 🚀 로컬 PostgreSQL로 빠르게 시작하기

## ⚡ 3분 내 실행하기

### 1️⃣ PostgreSQL 데이터베이스 생성 (30초)

```bash
# PowerShell에서
psql -U postgres -c "CREATE DATABASE question_bank;"
```

### 2️⃣ 프로젝트 설정 (1분)

```bash
# 프로젝트 폴더로 이동
cd question_bank_system

# 환경 파일 생성
cp .env.example .env

# .env 파일 수정 (기본값이 맞으면 그대로)
# DATABASE_URL=postgresql://postgres:postgres@localhost:5432/question_bank
```

### 3️⃣ 샘플 데이터 생성 및 실행 (1분)

```bash
# 가상환경 활성화 (이미 했으면 생략)
venv\Scripts\activate

# 테이블 및 샘플 데이터 생성
python init_local_db.py

# Backend 실행
python main.py
```

### 4️⃣ Frontend 실행 (다른 터미널에서)

```bash
cd frontend
npm install  # 첫 실행일 때만
npm run dev
```

---

## 📍 접근 주소

| 서비스 | URL |
|--------|-----|
| **Frontend** | http://localhost:3000 |
| **Backend API** | http://localhost:8000 |
| **API 문서** | http://localhost:8000/docs |
| **Health Check** | http://localhost:8000/health |

---

## ✅ 설정 확인

### PostgreSQL 연결 테스트

```bash
python -c "
from models import engine
try:
    with engine.connect() as conn:
        print('✅ PostgreSQL 연결 성공!')
except Exception as e:
    print('❌ 연결 실패:', e)
"
```

### 데이터베이스 테이블 확인

```bash
# 테이블 생성 확인
psql -U postgres -d question_bank -c "\dt"

# 과목 데이터 확인
psql -U postgres -d question_bank -c "SELECT * FROM subjects;"
```

---

## 🔄 기본 작업 흐름

### 1️⃣ Backend에서 과목 생성

Swagger UI (http://localhost:8000/docs)에서:

```
POST /api/subjects
Body:
{
  "name": "Python",
  "description": "Python 프로그래밍"
}
```

### 2️⃣ Excel 파일 업로드

Swagger UI에서:

```
POST /api/files/upload/excel
- file: questions.xlsx
- subject_id: 1
```

### 3️⃣ 코드 파일 업로드 (AI 문제 생성)

Swagger UI에서:

```
POST /api/files/upload/code
- file: sample.java
- subject_id: 1
- auto_generate: true
```

### 4️⃣ 랜덤 문제 출제

Swagger UI에서:

```
POST /api/questions/random/quiz
Body:
{
  "subject_id": 1,
  "difficulty": "MEDIUM",
  "count": 5
}
```

---

## 🔧 비밀번호가 다른 경우

PostgreSQL 설치 시 다른 비밀번호를 설정했다면:

```bash
# .env 파일 수정
DATABASE_URL=postgresql://postgres:YOUR_PASSWORD@localhost:5432/question_bank
```

**YOUR_PASSWORD**를 실제 비밀번호로 바꾸세요!

---

## 🛠️ 자주 사용하는 명령어

```bash
# Backend 재시작
python main.py

# Frontend 재시작
cd frontend && npm run dev

# 데이터베이스 초기화 (모든 데이터 삭제)
python init_local_db.py

# 특정 테이블 조회
psql -U postgres -d question_bank -c "SELECT * FROM questions LIMIT 5;"

# 로그 확인
# Frontend: 브라우저 F12 → Console
# Backend: 터미널 출력 확인
```

---

## ❌ 문제 해결

### PostgreSQL 서비스가 실행 중이 아님
```bash
# 상태 확인
Get-Service PostgreSQL*

# 시작
Start-Service PostgreSQL*
```

### 비밀번호 오류
```bash
# pgAdmin에서 postgres 유저 비밀번호 변경
# 또는 터미널에서
psql -U postgres -c "ALTER USER postgres WITH PASSWORD 'new_password';"
```

### 데이터베이스가 없음
```bash
psql -U postgres -c "CREATE DATABASE question_bank;"
```

### 테이블 재생성
```bash
# 기존 테이블 삭제 후 재생성
python init_local_db.py
```

---

## 📚 다음 단계

- [ ] 모든 API 엔드포인트 테스트
- [ ] 파일 업로드 기능 검증
- [ ] OpenAI API 연동 확인
- [ ] 배포 준비 ([DEPLOYMENT_STRATEGY.md](./DEPLOYMENT_STRATEGY.md) 참고)

---

## 💡 팁

1. **Swagger UI 활용** - http://localhost:8000/docs에서 모든 API 테스트 가능
2. **pgAdmin 사용** - 데이터베이스 시각적 관리 (Windows Start에서 "pgAdmin" 검색)
3. **로그 확인** - 터미널에서 Backend 로그 실시간 확인
4. **핫 리로드** - 코드 수정 시 자동 재시작 (main.py의 --reload 옵션)

---

## 🎉 준비 완료!

이제 로컬 PostgreSQL 환경에서 완전한 문제 은행 시스템을 개발할 수 있습니다!
