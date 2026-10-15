from fastapi import FastAPI, Depends, HTTPException, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from contextlib import asynccontextmanager
import os

from config import settings
from models import create_tables, get_db, engine, Base
from routes import auth, progress, questions, files, recommendations, subjects, public_exams

# 스타트업 이벤트 (Vercel 예외 처리 적용)
@asynccontextmanager
async def lifespan(app: FastAPI):
    # 시작
    print("서버 시작: 데이터베이스 연결 확인...")
    try:
        # DB 테이블 생성 시도 (이미 생성되어 있다면 통과)
        create_tables()
        print("데이터베이스 초기화 완료")
    except Exception as e:
        print(f"DB 초기화 중 경고/에러 발생 (Vercel 환경 체크 필요): {e}")

    # Vercel 읽기 전용 파일 시스템 대응 (임시 폴더 /tmp 사용 또는 실패 무시)
    try:
        if not os.path.exists(settings.UPLOAD_DIR):
            os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
    except Exception as e:
        print(f"업로드 디렉토리 생성 스킵 (Serverless Read-Only Environment): {e}")
    
    yield
    
    # 종료
    print("서버 종료")

# FastAPI 앱 생성
app = FastAPI(
    title="Question Bank System API",
    description="Excel 및 코드 기반 문제 은행 시스템",
    version="1.0.0",
    lifespan=lifespan
)

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS if hasattr(settings, 'CORS_ORIGINS') else ["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 라우트 등록
app.include_router(questions.router, prefix="/api/questions", tags=["Questions"])
app.include_router(files.router, prefix="/api/files", tags=["Files"])
app.include_router(subjects.router, prefix="/api/subjects", tags=["Subjects"])
app.include_router(auth.router, prefix="/api/auth", tags=["Authentication"])
app.include_router(progress.router, prefix="/api/progress", tags=["Progress"])
app.include_router(recommendations.router, prefix="/api/recommendations", tags=["Recommendations"])
app.include_router(public_exams.router, prefix="/api/public-exams", tags=["Public Exams"])

# 헬스 체크
@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "version": "1.0.0"
    }

# 루트 경로
@app.get("/")
async def root():
    return {
        "message": "Question Bank System API",
        "docs": "/docs",
        "redoc": "/redoc"
    }

# ⚠️ Vercel 배포를 위해 uvicorn.run(...) 부분은 완전히 삭제하거나 주석 처리합니다.
# (Vercel이 app 객체를 직접 인스턴스화하여 서빙합니다)
