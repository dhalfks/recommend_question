# 🐘 PostgreSQL 로컬 설정 완료!

## ✅ 변경 사항 요약

### config.py 수정
```python
# 기존 (SQLite)
DATABASE_URL = "sqlite:///./test.db"

# 변경됨 (PostgreSQL)
DATABASE_URL = "postgresql://postgres:postgres@localhost:5432/question_bank"
```

### .env.example 업데이트
```env
# PostgreSQL 로컬 연결 정보
DATABASE_URL=postgresql://postgres:YOUR_PASSWORD@localhost:5432/question_bank
```

### models.py 최적화
```python
# PostgreSQL 특화 설정 추가
pool_pre_ping=True      # 연결 유효성 확인
pool_recycle=3600       # 1시간마다 연결 재생성
```

---

## 🚀 지금 바로 시작하기

### 1️⃣ 데이터베이스 생성 (복사 & 붙여넣기)

```bash
psql -U postgres -c "CREATE DATABASE question_bank;"
```

### 2️⃣ 환경 파일 설정

```bash
cd question_bank_system
cp .env.example .env
```

기본값이 맞으면 .env 파일을 수정할 필요 없습니다.  
PostgreSQL 비밀번호가 다른 경우만 수정하세요.

### 3️⃣ 데이터베이스 초기화

```bash
# 가상환경 활성화 (이미 했으면 생략)
venv\Scripts\activate

# 테이블 및 샘플 데이터 생성
python init_local_db.py
```

### 4️⃣ Backend 시작

```bash
python main.py
```

### 5️⃣ Frontend 시작 (다른 터미널)

```bash
cd frontend
npm install  # 첫 번만
npm run dev
```

---

## 🎯 접근 주소

| 항목 | URL |
|------|-----|
| Frontend | http://localhost:3000 |
| Backend API | http://localhost:8000 |
| Swagger UI | http://localhost:8000/docs |
| Health Check | http://localhost:8000/health |

---

## 📚 관련 문서

| 문서 | 설명 |
|------|------|
| **QUICK_START.md** | ⭐ 3분 내 실행하기 (가장 빠름) |
| **POSTGRESQL_SETUP_FINAL.md** | PostgreSQL 상세 체크리스트 |
| **LOCAL_POSTGRESQL_SETUP.md** | PostgreSQL 심화 가이드 |
| **DEPLOYMENT_STRATEGY.md** | 배포 전략 및 계획 |

---

## ✨ 주요 포인트

### ✅ PostgreSQL 기본값
```
호스트: localhost
포트: 5432
유저: postgres
비밀번호: postgres (설치 시 설정)
데이터베이스: question_bank
```

### ✅ 환경 변수 자동 설정
- `config.py`에서 기본값으로 자동 설정됨
- `.env` 파일 생성 후 필요시 수정

### ✅ 샘플 데이터 자동 생성
- `init_local_db.py` 실행 시 자동 생성
- 3개 과목, 9개 문제 포함

### ✅ 완전한 기능 지원
- Excel 파일 업로드
- 코드 파일 업로드 (OpenAI API)
- 랜덤 문제 출제
- 사용자 풀이 기록

---

## 🔧 일반적인 설정

### PostgreSQL 비밀번호가 다른 경우

```bash
# .env 파일 수정
DATABASE_URL=postgresql://postgres:YOUR_PASSWORD@localhost:5432/question_bank
```

### PostgreSQL 포트가 다른 경우

```bash
# 포트 확인
psql -U postgres -l

# .env 파일 수정 (예: 포트 5433)
DATABASE_URL=postgresql://postgres:postgres@localhost:5433/question_bank
```

### PostgreSQL이 다른 호스트에 있는 경우

```bash
# .env 파일 수정
DATABASE_URL=postgresql://postgres:postgres@remote-host.com:5432/question_bank
```

---

## ✅ 검증 체크리스트

다음 명령어로 설정 확인:

```bash
# 1. PostgreSQL 서비스 실행 확인
Get-Service PostgreSQL*

# 2. 데이터베이스 존재 확인
psql -U postgres -l | grep question_bank

# 3. 테이블 생성 확인
psql -U postgres -d question_bank -c "\dt"

# 4. 샘플 데이터 확인
psql -U postgres -d question_bank -c "SELECT COUNT(*) FROM questions;"

# 5. Backend 연결 확인
curl http://localhost:8000/health
```

---

## 🎉 완료!

이제 로컬 PostgreSQL 환경에서 완벽하게 작동합니다.

다음 단계:
- [ ] QUICK_START.md 읽기
- [ ] Frontend 실행
- [ ] API 테스트
- [ ] 배포 준비 ([DEPLOYMENT_STRATEGY.md](./DEPLOYMENT_STRATEGY.md))

---

## 📞 문제 해결

### PostgreSQL 서비스 시작
```bash
Start-Service PostgreSQL*
```

### 데이터베이스 재생성
```bash
# 삭제
psql -U postgres -c "DROP DATABASE IF EXISTS question_bank;"

# 생성
psql -U postgres -c "CREATE DATABASE question_bank;"

# 테이블 및 데이터 생성
python init_local_db.py
```

### 연결 오류 해결
- 비밀번호 확인: .env 파일
- 서비스 상태 확인: `Get-Service PostgreSQL*`
- 포트 확인: `psql -U postgres -l` 또는 pgAdmin

---

**🚀 이제 시작하세요!**
