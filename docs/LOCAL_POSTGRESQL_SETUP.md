# 로컬 PostgreSQL 설정 가이드

## ✅ PostgreSQL 설치 확인

### Windows
```bash
# PowerShell에서 확인
psql --version

# 출력 예시:
# psql (PostgreSQL) 15.3
```

### 로컬 PostgreSQL 연결 정보
```
호스트: localhost (또는 127.0.0.1)
포트: 5432 (기본값)
유저: postgres
비밀번호: PostgreSQL 설치 시 입력한 비밀번호
```

---

## 🔧 Step 1: PostgreSQL 서버 시작

### Windows (서비스로 실행)
```bash
# PostgreSQL 서비스는 Windows 설치 시 자동 시작됨
# 확인:
Get-Service PostgreSQL*
```

### 명령 프롬프트로 시작 (필요시)
```bash
# PostgreSQL이 설치된 경로로 이동
cd "C:\Program Files\PostgreSQL\15\bin"

# PostgreSQL 서버 시작 (이미 실행 중이면 생략 가능)
```

---

## 📝 Step 2: 데이터베이스 생성

### 방법 1: pgAdmin (GUI - 권장)

```
1. pgAdmin 열기 (Windows Start 메뉴에서 검색)
2. 왼쪽 트리에서 "Servers" → "PostgreSQL 15" 클릭
3. 비밀번호 입력 (PostgreSQL 설치 시 비밀번호)
4. "Databases" 우클릭 → "Create" → "Database"
5. Database name: question_bank
6. 생성
```

### 방법 2: psql 명령줄

```bash
# PowerShell에서
psql -U postgres

# psql 프롬프트에서
CREATE DATABASE question_bank;

# 확인
\l

# 나가기
\q
```

---

## 🏗️ Step 3: 스키마 생성

### 방법 1: Python 자동 생성 (권장)

```bash
# question_bank_system 폴더에서
python init_local_db.py
```

응답 예시:
```
📚 로컬 데이터베이스 초기화 중...
✅ 테이블 생성 완료
✅ 3개 과목 생성 완료
✅ 샘플 문제 생성 완료

📊 데이터베이스 통계:
   - 과목: 3개
   - 문제: 9개

📈 난이도별 문제:
   - EASY: 3개
   - MEDIUM: 6개
   - HARD: 0개

✨ 로컬 DB 초기화 완료!

🚀 다음 명령으로 서버를 시작하세요:
   python main.py
```

### 방법 2: SQL 스크립트 직접 실행

```bash
# PowerShell에서
psql -U postgres -d question_bank -f schema.sql
```

---

## 🔐 Step 4: .env 파일 설정

### .env 파일 생성

```bash
# 프로젝트 폴더에서
cp .env.example .env
```

### .env 파일 수정

```env
# PostgreSQL 로컬 연결
DATABASE_URL=postgresql://postgres:YOUR_PASSWORD@localhost:5432/question_bank

# OpenAI API (선택)
OPENAI_API_KEY=your_api_key

# 나머지는 기본값 사용
SERVER_HOST=0.0.0.0
SERVER_PORT=8000
```

**주의**: YOUR_PASSWORD를 PostgreSQL 설치 시 입력한 비밀번호로 바꾸세요!

---

## ✅ Step 5: 연결 테스트

### Python에서 연결 확인

```bash
# question_bank_system 폴더에서
python -c "
from config import settings
from models import engine
print('DATABASE_URL:', settings.DATABASE_URL)
try:
    with engine.connect() as conn:
        print('✅ PostgreSQL 연결 성공!')
except Exception as e:
    print('❌ 연결 실패:', e)
"
```

### psql로 직접 확인

```bash
psql -U postgres -d question_bank -c "\dt"
```

응답 예시:
```
          List of relations
 Schema |      Name       | Type  | Owner
--------+-----------------+-------+----------
 public | code_files      | table | postgres
 public | excel_questions | table | postgres
 public | questions       | table | postgres
 public | subjects        | table | postgres
 public | user_progress   | table | postgres
(5 rows)
```

---

## 🚀 Step 6: 애플리케이션 시작

```bash
# 가상환경 활성화 (이미 했으면 생략)
venv\Scripts\activate

# Backend 시작
python main.py

# 출력 예시:
# INFO:     Application startup complete
# Uvicorn running on http://0.0.0.0:8000
```

### API 확인

```
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc
- Health Check: http://localhost:8000/health
```

---

## 🔧 연결 정보 변경 (필요시)

비밀번호나 포트가 다른 경우:

```env
# 예시 1: 포트가 5433인 경우
DATABASE_URL=postgresql://postgres:password@localhost:5433/question_bank

# 예시 2: 유저명이 다른 경우
DATABASE_URL=postgresql://myuser:password@localhost:5432/question_bank

# 예시 3: 원격 PostgreSQL
DATABASE_URL=postgresql://user:password@remote-host.com:5432/question_bank
```

---

## ❌ 트러블슈팅

### 연결 오류 1: "psql: command not found"
**해결**: PostgreSQL bin 폴더를 PATH에 추가
```bash
# PowerShell
$env:Path += ";C:\Program Files\PostgreSQL\15\bin"
```

### 연결 오류 2: "password authentication failed"
**해결**: .env 파일의 비밀번호 확인
```bash
# 비밀번호 리셋 (Windows)
# 1. pgAdmin에서 postgres 유저 우클릭
# 2. Properties → Password 변경
# 3. .env 파일 업데이트
```

### 연결 오류 3: "could not connect to server"
**해결**: PostgreSQL 서비스 상태 확인
```bash
Get-Service PostgreSQL*

# 응답이 "Running"이어야 함
# "Stopped"이면 시작:
Start-Service "PostgreSQL*"
```

### 연결 오류 4: "database 'question_bank' does not exist"
**해결**: 데이터베이스 생성
```bash
psql -U postgres -c "CREATE DATABASE question_bank;"
python init_local_db.py  # 테이블 생성
```

---

## 📊 pgAdmin으로 데이터 확인

```
1. pgAdmin 열기
2. Servers → PostgreSQL 15 → Databases → question_bank
3. Schemas → public → Tables
4. 테이블 이름 우클릭 → View/Edit Data
```

---

## 💡 유용한 SQL 명령어

```bash
# 데이터베이스 목록
psql -U postgres -l

# 테이블 목록
psql -U postgres -d question_bank -c "\dt"

# 특정 테이블 데이터 조회
psql -U postgres -d question_bank -c "SELECT * FROM subjects;"

# 테이블 삭제 (초기화)
psql -U postgres -d question_bank -c "DROP TABLE IF EXISTS user_progress, excel_questions, code_files, questions, subjects CASCADE;"

# 데이터베이스 삭제
psql -U postgres -c "DROP DATABASE question_bank;"
```

---

## 📝 빠른 설정 요약

```bash
# 1. PostgreSQL 서버 실행 중 확인
Get-Service PostgreSQL*

# 2. 데이터베이스 생성
psql -U postgres -c "CREATE DATABASE question_bank;"

# 3. .env 파일 설정
cp .env.example .env
# .env 파일 편집: DATABASE_URL 설정

# 4. Python 모듈 설치 (이미 했으면 생략)
pip install -r requirements.txt

# 5. 테이블 생성 및 샘플 데이터 추가
python init_local_db.py

# 6. Backend 시작
python main.py

# 7. Frontend 시작 (다른 터미널)
cd frontend
npm run dev
```

---

## 🎯 다음 단계

- [x] PostgreSQL 로컬 설정 완료
- [ ] Backend 시작
- [ ] Frontend 시작
- [ ] API 테스트
- [ ] 배포 준비
