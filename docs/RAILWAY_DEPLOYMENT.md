# Railway 배포 가이드

## 빠른 배포 (3단계)

### 1️⃣ GitHub에 코드 푸시

```bash
# 저장소 초기화 (이미 되어있으면 생략)
git init
git add .
git commit -m "Initial commit: Question Bank System"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/question_bank_system.git
git push -u origin main
```

### 2️⃣ Railway 배포 설정

1. [Railway.app](https://railway.app/)에 로그인 (GitHub으로 가입)
2. "Start a New Project" 클릭
3. "Deploy from GitHub repo" 선택
4. 저장소 선택: `question_bank_system`
5. 배포 설정:
   - **Root Directory**: `question_bank_system` (또는 비워둠)
   - **Framework**: Python
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn main:app --host 0.0.0.0 --port $PORT`

### 3️⃣ 환경 변수 설정

Railway 대시보드에서 "Variables" 탭:

```env
DATABASE_URL=postgresql://user:password@neon-host/db_name
OPENAI_API_KEY=your_gemini_api_key
SERVER_HOST=0.0.0.0
SERVER_PORT=8000
CORS_ORIGINS=["https://your-frontend.vercel.app"]
```

---

## 상세 배포 단계

### Step 1: 데이터베이스 준비

#### Neon PostgreSQL 설정
```
1. neon.tech에서 무료 계정 생성
2. 새 프로젝트 생성 (PostgreSQL 15)
3. Connection String 복사:
   postgresql://user:password@neon-host/db_name
4. Railway 환경변수에 DATABASE_URL로 설정
```

### Step 2: Dockerfile 확인

프로젝트 루트에 `Dockerfile`이 있는지 확인:
- ✅ 있으면: Railway가 자동으로 사용
- ❌ 없으면: 위의 Dockerfile 참고

### Step 3: 배포 모니터링

```
1. Railway 대시보드에서 배포 진행 상태 확인
2. 빌드 로그 확인
3. 배포 완료 후 자동으로 URL 생성
```

---

## 배포 후 확인

### Health Check
```bash
curl https://your-railway-url.railway.app/health
```

Response:
```json
{
  "status": "healthy",
  "version": "1.0.0"
}
```

### API 문서
```
https://your-railway-url.railway.app/docs
```

### 테스트
```bash
# 과목 조회
curl https://your-railway-url.railway.app/api/subjects

# 문제 생성
curl -X POST https://your-railway-url.railway.app/api/questions \
  -H "Content-Type: application/json" \
  -d '{"subject_id": 1, "title": "Test", "content": "Test content", "difficulty": "EASY"}'
```

---

## 트러블슈팅

### 빌드 실패 (ModuleNotFoundError)

**증상**: `ModuleNotFoundError: No module named 'fastapi'`

**해결**:
```bash
# requirements.txt 확인
cat requirements.txt

# 필요한 패키지 모두 있는지 확인
pip freeze > requirements.txt  # 로컬에서 재생성
git add requirements.txt
git commit -m "Update requirements"
git push
```

### 데이터베이스 연결 오류

**증상**: `psycopg2.OperationalError: could not connect to server`

**해결**:
1. DATABASE_URL 확인
2. Neon 대시보드에서 IP whitelist 확인
3. 연결 문자열 형식 확인: `postgresql://user:password@host:port/database`

### PORT 바인딩 오류

**증상**: `Address already in use`

**해결**: 
- Railway에서 `--port $PORT` 사용 확인
- 환경변수 `PORT` 자동 설정됨

### 타임아웃 오류

**증상**: `504 Gateway Timeout`

**해결**:
1. 함수가 오래 걸리는지 확인 (OpenAI API 호출 등)
2. 타임아웃 시간 증가 (필요시)
3. 백그라운드 작업 고려

---

## 로컬에서 Docker 테스트 (선택사항)

```bash
# Docker 이미지 빌드
docker build -t question-bank .

# 로컬에서 실행 (SQLite)
docker run -p 8000:8000 question-bank

# PostgreSQL로 실행
docker run -p 8000:8000 \
  -e DATABASE_URL="postgresql://..." \
  -e OPENAI_API_KEY="..." \
  question-bank
```

---

## 자동 배포 설정

Railway는 GitHub 자동 배포를 지원합니다:

1. GitHub에 푸시하면 자동으로 빌드 시작
2. 빌드 성공 시 자동 배포
3. 배포 중에도 이전 버전 서비스 유지

---

## 비용 참고

**Railway 무료 플랜**:
- 월 $5 크레딧 (약 10시간 소규모 앱 실행 가능)
- 데이터베이스 비용 포함
- 충분한 테스트 및 학습용

---

## 다음 단계

- [ ] 데이터베이스 백업 설정
- [ ] 모니터링 대시보드 구성
- [ ] 로그 분석
- [ ] CDN 설정 (이미지 최적화)
- [ ] SSL 인증서 (자동)
