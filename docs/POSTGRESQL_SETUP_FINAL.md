# PostgreSQL 로컬 설정 - 최종 체크리스트

## ✅ Pre-Setup 확인사항

- [ ] PostgreSQL 설치 완료
- [ ] psql 명령어 실행 가능
- [ ] pgAdmin 설치 (선택사항, 권장)

---

## 🚀 설정 단계별 가이드

### Step 1: PostgreSQL 서비스 시작 확인 ⏱️ 30초

```bash
# PowerShell에서
Get-Service PostgreSQL*
```

**상태 확인**:
- ✅ **Running** → 정상 (다음 단계로)
- ❌ **Stopped** → 시작 필요:
  ```bash
  Start-Service PostgreSQL*
  ```

---

### Step 2: 데이터베이스 생성 ⏱️ 30초

```bash
psql -U postgres -c "CREATE DATABASE question_bank;"
```

**확인**:
```bash
psql -U postgres -l
# question_bank 데이터베이스가 목록에 보여야 함
```

---

### Step 3: 프로젝트 환경 설정 ⏱️ 1분

```bash
# 프로젝트 폴더로 이동
cd question_bank_system

# 환경 파일 생성
cp .env.example .env

# .env 파일 내용 확인
cat .env
```

**확인사항**:
```env
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/question_bank
```

비밀번호가 다른 경우만 수정:
```
DATABASE_URL=postgresql://postgres:YOUR_PASSWORD@localhost:5432/question_bank
```

---

### Step 4: Python 의존성 설치 ⏱️ 2-3분

```bash
# 가상환경 활성화 (이미 했으면 생략)
venv\Scripts\activate

# 의존성 설치
pip install -r requirements.txt
```

---

### Step 5: 데이터베이스 초기화 ⏱️ 30초

```bash
python init_local_db.py
```

**예상 출력**:
```
📚 로컬 데이터베이스 초기화 중...
✅ 테이블 생성 완료
✅ 3개 과목 생성 완료
✅ 샘플 문제 생성 완료

📊 데이터베이스 통계:
   - 과목: 3개
   - 문제: 9개

✨ 로컬 DB 초기화 완료!
```

---

### Step 6: Backend 시작 ⏱️ 즉시

```bash
python main.py
```

**성공 표시**:
```
INFO:     Application startup complete
Uvicorn running on http://0.0.0.0:8000
```

---

### Step 7: 연결 확인 ⏱️ 30초

**브라우저에서**:
- http://localhost:8000/health → `{"status": "healthy"}`
- http://localhost:8000/docs → Swagger UI 표시

**또는 다른 터미널에서**:
```bash
curl http://localhost:8000/health
```

---

## 🎯 총 소요 시간: ~5-8분

| 단계 | 작업 | 시간 |
|------|------|------|
| 1 | PostgreSQL 서비스 확인 | 30초 |
| 2 | 데이터베이스 생성 | 30초 |
| 3 | 환경 설정 | 1분 |
| 4 | 의존성 설치 | 2-3분 |
| 5 | DB 초기화 | 30초 |
| 6 | Backend 시작 | 즉시 |
| 7 | 연결 확인 | 30초 |
| **합계** | | **5-8분** |

---

## 📋 설정 완료 후 확인 목록

```bash
# 1. PostgreSQL 연결 확인
python -c "from models import engine; print('✅ DB 연결 OK' if engine else '❌ 실패')"

# 2. 테이블 생성 확인
psql -U postgres -d question_bank -c "\dt"

# 3. 샘플 데이터 확인
psql -U postgres -d question_bank -c "SELECT COUNT(*) as question_count FROM questions;"

# 4. API 응답 확인
curl http://localhost:8000/api/subjects
```

---

## 🔐 PostgreSQL 비밀번호 변경 (필요시)

### 현재 비밀번호가 "postgres"가 아닌 경우

**방법 1: pgAdmin 사용**
```
1. pgAdmin 열기
2. Servers 우클릭 → Register → Server
3. Connection 탭에서 비밀번호 입력
4. 저장
```

**방법 2: psql 사용**
```bash
# 현재 유저 비밀번호 변경
psql -U postgres -c "ALTER USER postgres WITH PASSWORD 'new_password';"

# .env 파일 업데이트
DATABASE_URL=postgresql://postgres:new_password@localhost:5432/question_bank
```

---

## 🚨 문제 발생 시

### 문제 1: "role 'postgres' does not exist"
```bash
# PostgreSQL이 제대로 설치되지 않음
# 재설치 필요
```

### 문제 2: "psql: command not found"
```bash
# PATH에 PostgreSQL bin 폴더 추가
$env:Path += ";C:\Program Files\PostgreSQL\15\bin"
```

### 문제 3: "password authentication failed"
```bash
# .env 파일의 비밀번호 확인
# DATABASE_URL을 올바르게 설정
```

### 문제 4: "could not translate host name 'localhost'"
```bash
# localhost 대신 127.0.0.1 사용
DATABASE_URL=postgresql://postgres:postgres@127.0.0.1:5432/question_bank
```

### 문제 5: "database 'question_bank' does not exist"
```bash
# 데이터베이스 생성
psql -U postgres -c "CREATE DATABASE question_bank;"

# 테이블 생성
python init_local_db.py
```

---

## 💾 데이터 백업 및 복원

### 데이터 백업
```bash
pg_dump -U postgres question_bank > backup.sql
```

### 데이터 복원
```bash
psql -U postgres question_bank < backup.sql
```

---

## 🔄 다시 시작하기

### 모든 데이터 삭제 후 재초기화
```bash
# 1. 데이터베이스 삭제
psql -U postgres -c "DROP DATABASE IF EXISTS question_bank;"

# 2. 데이터베이스 재생성
psql -U postgres -c "CREATE DATABASE question_bank;"

# 3. 테이블 및 샘플 데이터 재생성
python init_local_db.py
```

---

## ✨ 완료 신호

다음이 모두 작동하면 성공입니다:

```bash
# 1. PostgreSQL 서비스 실행 중
Get-Service PostgreSQL*

# 2. 데이터베이스 접근 가능
psql -U postgres -d question_bank -c "SELECT 1;"

# 3. Python에서 연결 가능
python -c "from models import SessionLocal; db = SessionLocal(); print('OK'); db.close()"

# 4. Backend API 응답
curl http://localhost:8000/api/subjects

# 5. Swagger UI 접근 가능
# 브라우저: http://localhost:8000/docs
```

---

## 📚 참고 문서

- [QUICK_START.md](./QUICK_START.md) - 빠른 시작 가이드
- [LOCAL_POSTGRESQL_SETUP.md](./LOCAL_POSTGRESQL_SETUP.md) - 상세 설정
- [README.md](./README.md) - 프로젝트 개요
- [DEPLOYMENT_STRATEGY.md](./DEPLOYMENT_STRATEGY.md) - 배포 전략

---

## 🎉 다음 단계

이 과정을 완료한 후:

1. ✅ Frontend 실행: `cd frontend && npm run dev`
2. ✅ API 테스트: http://localhost:8000/docs
3. ✅ 기능 검증: 파일 업로드, 문제 출제 등
4. ✅ 배포 준비: [DEPLOYMENT_STRATEGY.md](./DEPLOYMENT_STRATEGY.md) 참고
