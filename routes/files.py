from fastapi import APIRouter, UploadFile, File, HTTPException, Depends, Form
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
import os
import shutil
from typing import Optional

from models import get_db, CodeFile, Subject, User, UserRole
from services.auth import require_roles
from config import settings
from services.excel_processor import process_excel_file
from services.file_processor import process_code_file, save_upload_file
from services.ai_usage import complete_ai_usage, reserve_ai_usage

router = APIRouter()

@router.get("/template/excel")
async def download_excel_template():
    template_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "sample.xlsx"))
    if not os.path.isfile(template_path):
        raise HTTPException(status_code=404, detail="Excel 샘플 파일을 찾을 수 없습니다.")
    return FileResponse(
        template_path,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        filename="sample.xlsx",
    )

# Excel 파일 업로드 및 처리
@router.post("/upload/excel")
async def upload_excel(
    file: UploadFile = File(...),
    subject_id: int = Form(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_roles(UserRole.PROFESSOR, UserRole.ADMIN)
    ),
):
    """
    Excel 파일을 업로드하고 문제 데이터를 데이터베이스에 저장
    """
    # 파일 검증
    if not file.filename or not file.filename.lower().endswith('.xlsx'):
        raise HTTPException(status_code=400, detail=".xlsx 파일만 업로드할 수 있습니다.")
    if file.size is not None and file.size > settings.MAX_FILE_SIZE:
        raise HTTPException(status_code=413, detail="파일 크기는 10MB 이하여야 합니다.")
    
    # 과목 존재 확인
    subject = db.query(Subject).filter(Subject.id == subject_id).first()
    if not subject:
        raise HTTPException(status_code=404, detail="Subject not found")
    
    try:
        # 파일 저장
        file_path = await save_upload_file(file, settings.UPLOAD_DIR)
        
        # Excel 파일 처리
        professor_id = current_user.id if current_user.role == UserRole.PROFESSOR else None
        result = await process_excel_file(file_path, subject_id, professor_id, db)
        if not result["success"]:
            detail = result["message"]
            if result.get("errors"):
                detail += " " + "; ".join(result["errors"][:5])
            raise HTTPException(status_code=400, detail=detail)
        
        return {
            "status": "success",
            "file_name": file.filename,
            "subject_id": subject_id,
            "questions_created": result["count"],
            "message": result["message"]
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# 코드 파일 업로드 및 문제 자동 생성
@router.post("/upload/code")
async def upload_code_file(
    file: UploadFile = File(...),
    subject_id: int = Form(...),
    auto_generate: bool = Form(True),
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_roles(UserRole.PROFESSOR, UserRole.ADMIN)
    ),
):
    """
    코드 파일을 업로드하고 OpenAI API를 사용해 자동으로 문제 생성
    """
    # 파일 확장자 검증
    if not file.filename:
        raise HTTPException(status_code=400, detail="파일 이름이 없습니다.")
    file_ext = os.path.splitext(file.filename)[1].lower()
    if file_ext not in ['.java', '.js', '.sql', '.txt', '.md']:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported file type. Allowed: {', '.join(settings.ALLOWED_FILE_EXTENSIONS)}"
        )
    if file.size is not None and file.size > settings.MAX_FILE_SIZE:
        raise HTTPException(status_code=413, detail="파일 크기는 10MB 이하여야 합니다.")
    
    # 과목 존재 확인
    subject = db.query(Subject).filter(Subject.id == subject_id).first()
    if not subject:
        raise HTTPException(status_code=404, detail="Subject not found")
    
    try:
        # 파일 저장
        file_path = await save_upload_file(file, settings.UPLOAD_DIR)
        
        # 파일 내용 읽기
        try:
            with open(file_path, 'r', encoding='utf-8-sig') as f:
                file_content = f.read()
        except UnicodeDecodeError:
            with open(file_path, 'r', encoding='cp949') as f:
                file_content = f.read()
        
        # 데이터베이스에 코드 파일 저장
        code_file = CodeFile(
            file_name=file.filename,
            file_path=file_path,
            file_type=file_ext[1:],  # 확장자에서 점 제거
            file_content=file_content,
            subject_id=subject_id,
            professor_id=(
                current_user.id if current_user.role == UserRole.PROFESSOR else None
            ),
        )
        db.add(code_file)
        db.commit()
        db.refresh(code_file)
        
        # 자동 문제 생성
        if auto_generate:
            from services.question_generator import generate_questions_from_code
            usage_event = reserve_ai_usage(db, current_user, "QUESTION_GENERATION")
            try:
                result = await generate_questions_from_code(
                    file_content,
                    file.filename,
                    subject_id,
                    file_ext[1:],
                    db,
                    current_user.id if current_user.role == UserRole.PROFESSOR else None,
                )
            except Exception:
                complete_ai_usage(
                    db, usage_event, succeeded=False, failure_code="QUESTION_GENERATION_ERROR"
                )
                raise
            complete_ai_usage(
                db,
                usage_event,
                succeeded=result["success"],
                usage=result.get("usage"),
                failure_code=None if result["success"] else "QUESTION_GENERATION_FAILED",
            )
            if not result["success"]:
                raise HTTPException(status_code=502, detail=result["message"])
            return {
                "status": "success",
                "file_name": file.filename,
                "subject_id": subject_id,
                "code_file_id": code_file.id,
                "questions_generated": result["count"],
                "message": result["message"],
                "questions": result["questions"],
            }
        
        return {
            "status": "success",
            "file_name": file.filename,
            "subject_id": subject_id,
            "code_file_id": code_file.id,
            "message": "Code file uploaded successfully"
        }
    except HTTPException:
        raise
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# 업로드된 파일 목록
@router.get("/list")
async def list_uploaded_files(
    subject_id: Optional[int] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_roles(UserRole.PROFESSOR, UserRole.ADMIN)
    ),
):
    """
    업로드된 코드 파일 목록 조회
    """
    query = db.query(CodeFile)
    if current_user.role == UserRole.PROFESSOR:
        query = query.filter(CodeFile.professor_id == current_user.id)
    
    if subject_id:
        query = query.filter(CodeFile.subject_id == subject_id)
    
    files = query.all()
    return {
        "files": [
            {
                "id": f.id,
                "file_name": f.file_name,
                "file_type": f.file_type,
                "subject_id": f.subject_id,
                "uploaded_at": f.uploaded_at
            } for f in files
        ]
    }

# 파일 삭제
@router.delete("/{file_id}")
async def delete_file(
    file_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_roles(UserRole.PROFESSOR, UserRole.ADMIN)
    ),
):
    """
    코드 파일 삭제
    """
    code_file = db.query(CodeFile).filter(CodeFile.id == file_id).first()
    if not code_file:
        raise HTTPException(status_code=404, detail="File not found")
    if (
        current_user.role == UserRole.PROFESSOR
        and code_file.professor_id != current_user.id
    ):
        raise HTTPException(status_code=404, detail="File not found")
    
    # 실제 파일 삭제
    try:
        if os.path.exists(code_file.file_path):
            os.remove(code_file.file_path)
    except:
        pass
    
    db.delete(code_file)
    db.commit()
    return {"message": "File deleted successfully"}
