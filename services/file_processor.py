import os
from fastapi import UploadFile
import shutil
from pathlib import Path
from config import settings

async def save_upload_file(file: UploadFile, upload_dir: str) -> str:
    """
    업로드된 파일을 저장하고 파일 경로 반환
    """
    os.makedirs(upload_dir, exist_ok=True)
    
    safe_name = Path(file.filename or "upload.txt").name
    file_path = os.path.join(upload_dir, safe_name)
    
    # 같은 이름의 파일 존재 시 덮어쓰기
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    return file_path

async def process_code_file(file_path: str, file_type: str) -> dict:
    """
    코드 파일을 읽고 처리
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        return {
            "success": True,
            "content": content,
            "file_type": file_type
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }
