# Next.js 프런트엔드 Vercel 배포

현재 운영 방식은 프런트엔드만 별도 Vercel 프로젝트로 배포하는 구조가 아닙니다. 저장소 루트의 `vercel.json`이 Next.js와 FastAPI를 하나의 Vercel 프로젝트에 함께 배포합니다.

전체 배포 절차는 [통합 배포 가이드](../docs/DEPLOYMENT.md)를 먼저 참고하세요.

## 현재 배포 설정

```text
GitHub Repository: 저장소 전체
Vercel Root Directory: 비워두기
Output Directory Override: 끄기
Configuration: 루트 vercel.json
```

라우팅:

```text
/api/*, /docs, /openapi.json → FastAPI
나머지 경로                  → Next.js
```

프런트 환경변수:

```env
NEXT_PUBLIC_API_URL=/api
```

통합 배포에서는 브라우저가 같은 Vercel 도메인의 FastAPI를 호출하므로 별도의 Railway URL을 넣지 않습니다.

## 로컬 개발

`frontend/.env.local`:

```env
NEXT_PUBLIC_API_URL=http://localhost:8000/api
```

실행:

```powershell
Set-Location frontend
npm install
npm run dev
```

브라우저에서 `http://localhost:3000`으로 접속합니다. FastAPI는 별도 터미널에서 실행합니다.

```powershell
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

## 배포 전 검사

```powershell
Set-Location frontend
npx tsc --noEmit
npm run build
```

Vercel에서는 개발 서버 명령인 `npm run dev`를 사용하지 않습니다. Next.js 빌드는 `npm run build`로 수행합니다.

## Vercel 환경변수

하나의 Vercel 프로젝트에 다음 값을 함께 설정합니다.

```env
NEXT_PUBLIC_API_URL=/api
DATABASE_URL=postgresql://...
JWT_SECRET_KEY=...
OPENAI_API_KEY=sk-...
UPLOAD_DIR=/tmp/uploads
```

`NEXT_PUBLIC_API_URL`은 빌드할 때 JavaScript 번들에 반영됩니다. 값을 변경한 뒤에는 캐시 없이 재배포해야 합니다.

## 배포

```powershell
git status
git add <변경한 파일>
git commit -m "update frontend"
git push origin main
```

Vercel이 `main` 브랜치의 새 커밋을 자동 배포합니다. 배포가 끝나면 해당 Deployment의 Visit 버튼으로 먼저 확인합니다.

## 배포 후 확인

브라우저 개발자 도구의 Network 탭에서 다음 요청을 확인합니다.

```text
/api/auth/me
/api/subjects
/api/progress/dashboard
/api/recommendations/peer-missed-units
/api/recommendations/my-wrong
```

정상적인 API 요청에는 로그인 후 다음 헤더가 포함됩니다.

```text
Authorization: Bearer <access_token>
```

## 학생 대시보드

기본 대시보드와 부가 요청은 서로 독립적으로 처리됩니다.

- 풀이 현황: `/api/progress/dashboard`
- 과목: `/api/subjects`
- 과목별 소제목: `/api/questions/subject-units`
- 유사 학습자 추천: `/api/recommendations/peer-missed-units`
- 내 오답: `/api/recommendations/my-wrong`

추천 요청이 실패하더라도 기본 풀이 현황과 과목 목록은 표시되어야 합니다.

과목과 문제 목록·등록 요청은 끝 슬래시 없이 호출합니다.

```text
/api/subjects
/api/questions
```

Vercel의 경로 정규화와 FastAPI의 자동 슬래시 리다이렉트가 충돌하지 않도록 프런트와 백엔드 경로를 동일하게 유지합니다.

## 주요 오류

### 빈 배포와 404

다음 로그는 실제 Next.js 빌드가 실행되지 않은 상태입니다.

```text
Build Completed in /vercel/output [수십 ms]
Skipping cache upload because no files were prepared
```

현재 통합 구조에서는 Root Directory를 `frontend`로 지정하지 말고 저장소 루트를 사용해야 합니다. 루트 `vercel.json`이 두 빌드를 모두 선언합니다.

### `public` Output Directory 오류

Next.js Output Directory를 `public`으로 지정하지 않습니다. Output Directory override를 끄고 Next.js 기본 출력을 사용합니다.

### API가 localhost를 호출함

운영 환경에서 다음 요청이 보이면 환경변수가 빌드에 반영되지 않은 것입니다.

```text
http://localhost:8000/api/...
```

Vercel에 다음 값을 설정하고 재배포합니다.

```env
NEXT_PUBLIC_API_URL=/api
```

### `307` 또는 `308`

Response의 `Location`을 확인합니다. `/subjects/`와 `/subjects`, `/questions/`와 `/questions` 사이를 반복하면 trailing slash 충돌입니다. 현재 클라이언트와 서버는 슬래시 없는 경로를 사용합니다.

### 요청이 약 10초 후 canceled

Axios 기본 제한시간이 10초이므로 서버 쿼리 성능과 Vercel Runtime Logs를 확인합니다. 제한시간만 늘리기보다 전체 테이블 조회와 N+1 쿼리를 먼저 제거합니다.

### 변경 후 이전 화면이 남음

최신 커밋이 Production에 배포됐는지 확인하고 강력 새로고침합니다.

```text
Windows: Ctrl + Shift + R
macOS: Command + Shift + R
```

## 프런트 단독 배포가 필요한 경우

프런트와 백엔드를 다시 분리하려면 별도의 Vercel 프로젝트를 만들고 Root Directory를 `frontend`로 지정할 수 있습니다. 이 경우 `NEXT_PUBLIC_API_URL`은 실제 백엔드의 절대 URL이어야 하며, 백엔드 CORS 설정에도 프런트 도메인을 추가해야 합니다.

현재 프로젝트의 기본 운영 방식은 통합 배포이므로 특별한 이유가 없다면 분리하지 않습니다.
