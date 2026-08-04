# Vercel Frontend 배포 가이드

## 빠른 배포 (3단계)

### 1️⃣ GitHub에 frontend 코드 푸시

```bash
cd frontend
git init
git add .
git commit -m "Initial commit: Question Bank Frontend"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/question_bank_frontend.git
git push -u origin main
```

**또는 monorepo 구조**:
```bash
# 프로젝트 루트에서
git add .
git commit -m "Add frontend"
git push
```

### 2️⃣ Vercel 배포

1. [Vercel](https://vercel.com/)에 로그인 (GitHub으로 가입)
2. "Add New..." → "Project"
3. GitHub 저장소 선택
4. 프로젝트 설정:
   - **Framework Preset**: Next.js
   - **Root Directory**: `frontend` (또는 비워둠)
   - **Build Command**: `npm run build`
   - **Output Directory**: `.next`
   - **Environment Variables**: 다음 단계에서 설정

### 3️⃣ 환경 변수 설정

Vercel 프로젝트 Settings → Environment Variables:

```env
NEXT_PUBLIC_API_URL=https://your-railway-url.railway.app/api
```

---

## 상세 배포 단계

### 프로젝트 구조 (monorepo)

```
question_bank_system/
├── main.py (backend)
├── requirements.txt
├── Dockerfile
├── frontend/ (Next.js 앱)
└── ...
```

### Vercel에서 Monorepo 설정

1. Vercel 대시보드에서 프로젝트 생성
2. GitHub 저장소 선택
3. "Edit" → "Root Directory" → `frontend` 선택
4. Environment Variables 추가

---

## 배포 후 확인

### 프론트엔드 URL
```
https://your-app-name.vercel.app
```

### API 연결 테스트

브라우저 개발자 도구 (F12) → Network:

```
1. "upload.tsx" 페이지 방문
2. 네트워크 탭에서 API 호출 확인
3. https://your-backend.railway.app/api/... 요청 확인
4. 200 응답 확인
```

### 오류 확인

```
1. Console 탭에서 에러 메시지 확인
2. CORS 오류시 Backend의 CORS_ORIGINS 설정 확인
3. 404 오류시 API URL 확인
```

---

## 트러블슈팅

### CORS 오류

**증상**: 
```
Access to XMLHttpRequest at 'https://backend...' from origin 'https://your-app.vercel.app'
has been blocked by CORS policy
```

**해결**:

Backend (Railway) 환경변수 수정:
```env
CORS_ORIGINS=["https://your-app-name.vercel.app"]
```

그 후 Railway에 다시 배포:
```bash
git push  # 자동 배포 실행
```

### API 연결 실패

**증상**: 
```
Failed to fetch from API
Error: (Network error, 404, etc)
```

**해결**:

1. `frontend/.env.local` 확인:
```env
NEXT_PUBLIC_API_URL=https://your-railway-url.railway.app/api
```

2. Vercel 환경변수 다시 설정
3. 프로젝트 재배포: Vercel 대시보드 → Redeploy

### 빌드 실패

**증상**: Build failed 표시

**해결**:
```bash
# 로컬에서 빌드 테스트
cd frontend
npm install
npm run build

# 오류 메시지 확인
npm run build 2>&1 | tail -50
```

---

## 성능 최적화

### Image Optimization

```tsx
// pages/upload.tsx에서
import Image from 'next/image'

<Image
  src="/logo.png"
  alt="Logo"
  width={200}
  height={100}
/>
```

### Bundle Analysis

```bash
npm install --save-dev @next/bundle-analyzer

# next.config.js에 추가
const withBundleAnalyzer = require('@next/bundle-analyzer')({
  enabled: process.env.ANALYZE === 'true',
})

module.exports = withBundleAnalyzer({...})

# 실행
ANALYZE=true npm run build
```

### ISR (Incremental Static Regeneration)

```tsx
// pages/quiz.tsx
export async function getStaticProps() {
  return {
    props: {
      // ...
    },
    revalidate: 60  // 60초마다 재생성
  }
}
```

---

## 배포 후 모니터링

### Vercel Analytics

1. Vercel 대시보드 → Analytics
2. 페이지 로드 시간
3. 사용자 경험 지표 (Core Web Vitals)
4. 지역별 성능

### Error Tracking

1. Vercel 대시보드 → Errors
2. 실시간 에러 알림
3. 스택 트레이스 확인

### 로그 확인

```bash
# Vercel CLI 설치
npm i -g vercel

# 로그 확인
vercel logs your-app-name
```

---

## 버전 업데이트

### 새 버전 배포

```bash
# 코드 수정
# ...

# GitHub에 푸시
git add .
git commit -m "Update: feature description"
git push

# Vercel이 자동으로 배포
# (Vercel 대시보드에서 진행 상황 확인)
```

### 롤백

1. Vercel 대시보드 → Deployments
2. 이전 버전 선택
3. "Promote to Production" 클릭

---

## 추가 기능

### Serverless Functions (API Routes)

`pages/api/` 폴더에 추가 가능:

```typescript
// pages/api/custom.ts
import type { NextApiRequest, NextApiResponse } from 'next'

export default function handler(
  req: NextApiRequest,
  res: NextApiResponse,
) {
  res.status(200).json({ message: 'Hello' })
}
```

### 사용자 정의 도메인

1. Vercel 대시보드 → Settings → Domains
2. 도메인 추가
3. DNS 설정 (자동 또는 수동)

### HTTPS 자동 설정

- Vercel에서 자동으로 Let's Encrypt 인증서 생성
- 모든 배포에 자동 적용

---

## 참고 자료

- [Vercel Next.js 배포](https://vercel.com/docs/frameworks/nextjs)
- [Vercel Environment Variables](https://vercel.com/docs/concepts/projects/environment-variables)
- [Next.js 성능 최적화](https://nextjs.org/learn/foundations/how-nextjs-works)

---

## 비용

**Vercel 무료 플랜**:
- 무제한 배포
- 자동 HTTPS
- 전역 CDN
- 무료 도메인 (vercel.app)
- 월 $0 (유료는 $20+)

---

## 다음 단계

- [ ] 커스텀 도메인 연결
- [ ] Analytics 설정
- [ ] Error tracking 설정
- [ ] Performance 모니터링
- [ ] A/B 테스팅 구성
