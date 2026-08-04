# 🚀 배포 전략 최종 정리

## 💡 권장: 로컬 DB 구성 후 배포

### 이유
1. ✅ **완전한 기능 검증** - 모든 기능을 로컬에서 테스트하고 배포
2. ✅ **환경 변수 미리 준비** - 배포 후 예상치 못한 오류 최소화
3. ✅ **빠른 디버깅** - 로컬에서 발견된 문제는 쉽게 수정
4. ✅ **비용 절감** - 배포 후 오류로 인한 비용 손실 방지

---

## 📋 최적 배포 절차 (4-5시간)

### Phase 1: 로컬 환경 완성 (2-3시간)

#### Step 1-1: Backend 로컬 테스트

```bash
# 1. 현재 디렉토리: question_bank_system

# 2. 가상환경 생성 및 활성화
python -m venv venv
venv\Scripts\activate  # Windows

# 3. 의존성 설치
pip install -r requirements.txt

# 4. 로컬 DB 초기화 (SQLite 자동 생성)
python init_local_db.py

# 5. Backend 시작
python main.py

# 6. 확인
# - http://localhost:8000 접근
# - http://localhost:8000/docs에서 API 테스트
```

#### Step 1-2: Frontend 로컬 테스트

```bash
# 1. 다른 터미널에서 frontend 폴더로 이동
cd frontend

# 2. 의존성 설치
npm install

# 3. Frontend 시작
npm run dev

# 4. 확인
# - http://localhost:3000 접근
# - 페이지 렌더링 확인
# - Backend API 호출 확인
```

#### Step 1-3: 통합 테스트 (필수 체크리스트)

```
☑ Backend API 모두 정상 작동
☑ Frontend 모든 페이지 로드
☑ 파일 업로드 기능 작동
☑ OpenAI API 호출 성공 (코드 파일 업로드 테스트)
☑ 랜덤 문제 출제 기능 작동
☑ 오류 메시지 표시 정상
```

---

### Phase 2: 클라우드 환경 준비 (1시간)

#### Step 2-1: Neon PostgreSQL 생성

```
1. https://neon.tech에서 무료 계정 생성
2. 새 프로젝트 생성 (PostgreSQL 15)
3. Connection String 복사 (예: postgresql://user:password@host/db)
4. 보관
```

#### Step 2-2: OpenAI API 키 확보

```
1. https://makersuite.google.com/app/apikey에서 API 키 생성
2. 복사 및 보관
```

#### Step 2-3: GitHub 저장소 준비

```bash
# 프로젝트 폴더에서
git init
git add .
git commit -m "Initial commit: Question Bank System"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/question-bank-system.git
git push -u origin main
```

---

### Phase 3: Backend 배포 (30분)

#### Railway 배포

```
1. https://railway.app에 로그인
2. "Start a New Project" → "Deploy from GitHub repo"
3. 저장소 선택
4. 자동 감지 후 배포 시작
5. 환경변수 설정:
   - DATABASE_URL=<Neon PostgreSQL 연결 문자열>
   - OPENAI_API_KEY=<Google OpenAI API 키>
   - CORS_ORIGINS=["https://your-frontend.vercel.app"]
6. 자동 배포 완료 (5-10분)
```

#### 배포 확인

```bash
# 생성된 URL 확인 (예: https://abc123.railway.app)
curl https://your-railway-url.railway.app/health

# 응답
# {"status": "healthy", "version": "1.0.0"}
```

---

### Phase 4: Frontend 배포 (20분)

#### Vercel 배포

```
1. https://vercel.com에 로그인
2. "Add New Project" → GitHub 저장소 선택
3. Framework: Next.js 선택
4. Root Directory: frontend 설정
5. 환경변수 설정:
   - NEXT_PUBLIC_API_URL=https://your-railway-url.railway.app/api
6. 자동 배포 (3-5분)
```

#### 배포 확인

```
생성된 URL: https://your-app-name.vercel.app
```

---

### Phase 5: 통합 테스트 (30분)

#### 배포된 서비스에서 테스트

```
1. Frontend 접속: https://your-app-name.vercel.app
2. 과목 목록 로드 확인
3. 파일 업로드 테스트
4. 문제 출제 테스트
5. 오류 발생 시 Backend 로그 확인
```

---

## 📊 비용 요약

| 서비스 | 무료 플랜 | 월 비용 |
|--------|----------|--------|
| **Railway (Backend)** | $5 크레딧 | $0 (테스트용 충분) |
| **Neon (PostgreSQL)** | 3 projects | $0 (무료) |
| **Vercel (Frontend)** | 무제한 배포 | $0 (무료) |
| **Google OpenAI API** | 월 60 호출 | $0 (테스트용 충분) |
| **총** | | **$0-5** |

---

## ⚠️ 주의사항

### Before 배포 (반드시 확인)

```
[ ] OPENAI_API_KEY 설정됨
[ ] DATABASE_URL 정확함 (포트, 유저명 등)
[ ] CORS_ORIGINS에 Frontend URL 포함
[ ] Frontend의 NEXT_PUBLIC_API_URL 정확함
[ ] 민감한 정보가 GitHub에 커밋되지 않음
[ ] .env 파일이 .gitignore에 있음
```

### After 배포 (배포 직후)

```
[ ] Backend API 응답 확인 (/health)
[ ] Frontend 페이지 로드 확인
[ ] API 연결 테스트 (F12 Network 탭)
[ ] 오류 로그 확인
[ ] 모니터링 설정
```

---

## 🔄 배포 후 업데이트 흐름

### 새 기능 추가/수정 시

```bash
# 1. 코드 수정
# 2. 로컬에서 테스트
# 3. GitHub에 푸시
git add .
git commit -m "기능 설명"
git push

# 4. 자동 배포 (Railway, Vercel이 자동으로 감지)
# 5. Vercel/Railway 대시보드에서 배포 확인
```

### 긴급 롤백

```
1. Railway 대시보드 → Builds
2. 이전 버전의 "Redeploy" 클릭

또는

1. Vercel 대시보드 → Deployments
2. 이전 버전 선택 → "Promote to Production"
```

---

## 📈 다음 개선 사항

- [ ] 사용자 인증 (JWT)
- [ ] 문제별 통계 대시보드
- [ ] 사용자 정의 도메인
- [ ] 이메일 알림 (문제 생성 완료 등)
- [ ] 캐싱 (Redis)
- [ ] 로그 분석
- [ ] A/B 테스팅

---

## 🎯 예상 일정

| 단계 | 시간 | 완료 |
|------|------|------|
| 로컬 환경 완성 | 2-3시간 | ⏳ |
| 클라우드 환경 준비 | 1시간 | ⏳ |
| Backend 배포 | 30분 | ⏳ |
| Frontend 배포 | 20분 | ⏳ |
| 통합 테스트 | 30분 | ⏳ |
| **총 시간** | **4-5시간** | |

---

## 💬 Q&A

### Q: 배포 전에 로컬에서 몇 시간을 써야 하나?
**A**: 처음 시도하면 2-3시간, 숙련되면 30분-1시간

### Q: 로컬 DB를 배포된 서버로 옮길 수 있나?
**A**: 가능하지만 권장하지 않음. 프로덕션은 처음부터 클라우드 DB 사용 권장

### Q: 배포 후 DB 오류가 나면?
**A**: DATABASE_URL 확인, Neon 대시보드에서 연결 상태 확인, Railway 로그 확인

### Q: 배포 후 CORS 오류 발생
**A**: Backend의 CORS_ORIGINS에 Frontend URL 추가, Railway 재배포

### Q: OpenAI API가 작동 안 함
**A**: API 키 확인, API 활성화 확인, 할당량 확인 (월 60호출 무료)

---

## 📚 참고 자료

- [LOCAL_TESTING.md](./LOCAL_TESTING.md) - 로컬 테스트 가이드
- [DEPLOYMENT_CHECKLIST.md](./DEPLOYMENT_CHECKLIST.md) - 체크리스트
- [RAILWAY_DEPLOYMENT.md](./RAILWAY_DEPLOYMENT.md) - Backend 배포
- [VERCEL_DEPLOYMENT.md](./frontend/VERCEL_DEPLOYMENT.md) - Frontend 배포

---

## ✨ 최종 확인

```
✅ 로컬 환경에서 모든 기능 테스트 완료
✅ 클라우드 리소스 생성 (DB, API 키)
✅ GitHub 저장소 준비
✅ Backend 배포 (Railway)
✅ Frontend 배포 (Vercel)
✅ 배포된 서비스 통합 테스트
✅ 모니터링 및 로그 확인

🎉 배포 완료!
```
