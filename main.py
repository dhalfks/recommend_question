from fastapi import FastAPI, Depends, HTTPException, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from contextlib import asynccontextmanager
import os

from config import settings
from models import create_tables, get_db, engine, Base
from routes import auth, progress, questions, files, recommendations, subjects

# 스타트업 이벤트
@asynccontextmanager
async def lifespan(app: FastAPI):
    # 시작
    print("서버 시작: 데이터베이스 테이블 생성 중...")
    create_tables()
    print("데이터베이스 초기화 완료")
    
    # 업로드 디렉토리 생성
    os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
    
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
    allow_origins=settings.CORS_ORIGINS,
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

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=settings.SERVER_HOST, port=settings.SERVER_PORT)
