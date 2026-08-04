# 문제 은행 시스템 - 배포 체크리스트

## ✅ Pre-Deployment Checklist

### 1️⃣ 로컬 환경 검증 (필수)

#### Backend
- [ ] Python 3.10+ 설치 확인
- [ ] 가상환경 활성화
- [ ] `pip install -r requirements.txt` 완료
- [ ] `.env` 파일 생성 및 설정
- [ ] `python main.py` 정상 실행
- [ ] http://localhost:8000/docs 접근 가능
- [ ] 각 API 엔드포인트 테스트 완료
  - [ ] GET /api/subjects
  - [ ] POST /api/subjects (과목 생성)
  - [ ] POST /api/files/upload/excel (Excel 파일)
  - [ ] POST /api/files/upload/code (코드 파일 + OpenAI API)
  - [ ] POST /api/questions/random/quiz (랜덤 출제)

#### Frontend
- [ ] Node.js 16+ 설치 확인
- [ ] `cd frontend && npm install` 완료
- [ ] `.env.local` 설정 (NEXT_PUBLIC_API_URL)
- [ ] `npm run dev` 정상 실행
- [ ] http://localhost:3000 접근 가능
- [ ] 각 페이지 렌더링 확인
  - [ ] 홈페이지
  - [ ] 파일 업로드 페이지
  - [ ] 문제 풀이 페이지
- [ ] API 연동 테스트
  - [ ] 과목 목록 로드
  - [ ] 파일 업로드
  - [ ] 문제 로드

#### 통합 테스트
- [ ] Frontend에서 Backend API 호출 성공
- [ ] 파일 업로드 완료 및 문제 생성 확인
- [ ] 랜덤 문제 출제 기능 테스트
- [ ] 오류 메시지 표시 정상 작동

---

### 2️⃣ 배포 전 준비

#### Backend (FastAPI)
- [ ] 모든 `print()` 디버그 코드 제거 또는 로거로 변경
- [ ] SECRET_KEY 등 민감 정보 환경변수로 관리
- [ ] CORS 설정 검토 (production URL 포함)
- [ ] 에러 핸들링 개선
- [ ] 로깅 설정 완료

#### Frontend (Next.js)
- [ ] `npm run build` 성공 확인
- [ ] 빌드 결과 오류 없음
- [ ] 환경 변수 올바르게 설정
- [ ] API URL이 프로덕션 주소로 설정
- [ ] 불필요한 console.log 제거

#### Database
- [ ] Neon/Supabase 프로젝트 생성 완료
- [ ] Connection String 확보
- [ ] schema.sql 파일 준비
- [ ] 데이터베이스 접근 테스트 완료

#### OpenAI API
- [ ] Google AI Studio에서 API 키 생성
- [ ] API 활성화 확인
- [ ] API 할당량 충분 확인

---

### 3️⃣ 배포 단계

#### Step 1: Backend 배포 (Railway 예시)
```
1. GitHub에 코드 커밋 및 푸시
2. Railway.app에서 로그인
3. 새 프로젝트 생성 → GitHub 저장소 선택
4. 배포 디렉토리 선택 (question_bank_system)
5. 환경 변수 설정:
   - DATABASE_URL=<Neon PostgreSQL Connection String>
   - OPENAI_API_KEY=<Your API Key>
   - CORS_ORIGINS=["https://your-frontend.vercel.app"]
6. 자동 배포 시작
7. 배포 완료 후 로그 확인
```

Deployment URL: `https://your-backend-api.railway.app`

#### Step 2: 클라우드 Database 마이그레이션
```
1. 배포된 Backend에서 POST /health 호출로 연결 확인
2. 필요시 테스트 데이터 추가
3. API 테스트 (Postman, Swagger)
```

#### Step 3: Frontend 배포 (Vercel)
```
1. GitHub에서 frontend 폴더를 root로 하는 새 저장소 생성
   또는 monorepo 설정
2. Vercel에서 로그인
3. GitHub 저장소 연결
4. 프로젝트 설정:
   - Framework: Next.js
   - Build Command: npm run build
   - Output Directory: .next
5. 환경 변수 설정:
   NEXT_PUBLIC_API_URL=https://your-backend-api.railway.app/api
6. 자동 배포
```

Deployment URL: `https://your-app-name.vercel.app`

---

### 4️⃣ 배포 후 검증

#### Backend 검증
- [ ] Health Check: `GET https://your-backend.railway.app/health`
- [ ] API 문서: `https://your-backend.railway.app/docs`
- [ ] 과목 조회: `GET /api/subjects`
- [ ] 파일 업로드 테스트: `POST /api/files/upload/code`
- [ ] 로그 확인 (Railway 콘솔)

#### Frontend 검증
- [ ] 프론트엔드 페이지 로드
- [ ] 과목 목록 표시
- [ ] 파일 업로드 기능 작동
- [ ] API 호출 성공
- [ ] 오류 콘솔 확인 (F12)

#### 통합 테스트
- [ ] 파일 업로드 → 데이터베이스 저장 확인
- [ ] 코드 파일 업로드 → OpenAI API 호출 → 문제 생성
- [ ] 랜덤 문제 출제
- [ ] 사용자 경험 테스트

---

### 5️⃣ 배포 후 모니터링

#### Railway 모니터링
- [ ] 로그 확인
- [ ] CPU/Memory 사용량
- [ ] 에러율
- [ ] API 응답 시간

#### Vercel 모니터링
- [ ] 빌드 로그
- [ ] 배포 상태
- [ ] 성능 지표
- [ ] 에러 트래킹

---

## 📋 추천 배포 순서 및 시간표

| 단계 | 작업 | 예상시간 | 상태 |
|------|------|--------|------|
| 1 | 로컬 환경 완성 (Backend + Frontend) | 2-3시간 | ⏳ |
| 2 | Neon/Supabase DB 생성 | 30분 | ⏳ |
| 3 | schema.sql 실행 | 10분 | ⏳ |
| 4 | Backend 배포 (Railway) | 30분 | ⏳ |
| 5 | Backend API 테스트 | 20분 | ⏳ |
| 6 | Frontend 배포 (Vercel) | 20분 | ⏳ |
| 7 | 통합 테스트 | 30분 | ⏳ |
| **총소요시간** | | **~4-5시간** | |

---

## 🔧 배포 후 트러블슈팅

### Backend 오류
| 증상 | 원인 | 해결 |
|------|------|------|
| 502 Bad Gateway | Backend 시작 실패 | 환경변수 확인, 로그 보기 |
| 404 Not Found | 라우트 없음 | API 엔드포인트 확인 |
| Connection refused | DB 연결 실패 | DATABASE_URL 확인 |
| 413 Payload Too Large | 파일 크기 초과 | MAX_FILE_SIZE 증가 |

### Frontend 오류
| 증상 | 원인 | 해결 |
|------|------|------|
| API 호출 실패 | CORS 설정 | CORS_ORIGINS 업데이트 |
| 404 페이지 | 라우트 설정 | Next.js 라우팅 확인 |
| 환경변수 미설정 | .env 누락 | NEXT_PUBLIC_API_URL 확인 |

---

## 📞 배포 리소스

### 공식 문서
- [Railway 배포 가이드](https://docs.railway.app/)
- [Vercel 배포 가이드](https://vercel.com/docs)
- [Neon PostgreSQL](https://neon.tech/docs)
- [FastAPI 배포](https://fastapi.tiangolo.com/deployment/)

### 대안 배포 서비스
- **Backend**: Heroku, Render, Fly.io
- **Frontend**: Netlify, GitHub Pages
- **Database**: AWS RDS, Google Cloud SQL, Azure Database

---

## ✨ 배포 완료 후 다음 단계

- [ ] 도메인 연결
- [ ] SSL 인증서 설정
- [ ] 백업 정책 수립
- [ ] 모니터링 대시보드 구성
- [ ] CI/CD 파이프라인 개선
- [ ] 사용자 피드백 수집
- [ ] 성능 최적화
