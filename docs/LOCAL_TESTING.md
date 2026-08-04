# 로컬 환경에서 빠르게 테스트하기

## 1. SQLite로 빠른 테스트 (권장)

config.py에 다음을 추가하면 SQLite로 즉시 테스트 가능:

```python
# config.py 수정
import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # 로컬 테스트용 SQLite
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL", 
        "sqlite:///./test.db"  # 로컬 테스트
    )
    
    OPENAI_API_KEY: str = ""
    # ... 나머지 설정
```

## 2. 설정 파일별 환경 변수

### 로컬 개발용 (.env.dev)
```env
DATABASE_URL=sqlite:///./test.db
OPENAI_API_KEY=your_api_key_here
SERVER_HOST=127.0.0.1
SERVER_PORT=8000
CORS_ORIGINS=["http://localhost:3000"]
```

### 클라우드 배포용 (.env.prod)
```env
DATABASE_URL=postgresql://user:password@neon-host/db
OPENAI_API_KEY=your_api_key_here
SERVER_HOST=0.0.0.0
SERVER_PORT=8000
CORS_ORIGINS=["https://yourapp.vercel.app"]
```

## 3. 로컬 테스트 체크리스트

- [ ] Backend 서버 정상 실행 (http://localhost:8000)
- [ ] Swagger UI 접근 가능 (http://localhost:8000/docs)
- [ ] 과목 생성 API 테스트
- [ ] Excel 파일 업로드 테스트
- [ ] 코드 파일 업로드 테스트 (OpenAI API)
- [ ] 랜덤 문제 출제 테스트
- [ ] Frontend 페이지 로딩 (http://localhost:3000)
- [ ] API 연결 테스트 (파일 업로드 등)

## 4. 데이터 마이그레이션 (SQLite → PostgreSQL)

로컬 테스트 완료 후 Neon PostgreSQL로 이동:

```bash
# 1. Neon에서 데이터베이스 생성
# 2. schema.sql 실행
# 3. 테스트 데이터 필요시 Python 스크립트로 마이그레이션

# 예: test.db → PostgreSQL로 데이터 이동
python scripts/migrate_db.py --from sqlite:///test.db --to postgresql://...
```

## 5. OpenAI API 테스트 팁

코드 파일 업로드 시 OpenAI API가 호출됩니다:

```bash
# Swagger UI에서 직접 테스트:
# POST /api/files/upload/code
# - file: sample.java (테스트 파일)
# - subject_id: 1
# - auto_generate: true

# 응답에서 questions_generated 확인
```
