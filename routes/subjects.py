from fastapi import APIRouter, Depends, HTTPException

from models import get_db, Subject, User, UserRole
from schemas.questions import SubjectCreate, SubjectResponse, SubjectUpdate
from services.auth import get_current_user, require_roles

router = APIRouter()

# 모든 과목 조회
@router.get("", response_model=list[SubjectResponse])
async def get_subjects(
    db=Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    subjects = db.query(Subject).all()
    return subjects

# 특정 과목 조회
@router.get("/{subject_id}", response_model=SubjectResponse)
async def get_subject(
    subject_id: int,
    db=Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    subject = db.query(Subject).filter(Subject.id == subject_id).first()
    if not subject:
        raise HTTPException(status_code=404, detail="Subject not found")
    return subject

# 과목 생성
@router.post("", response_model=SubjectResponse)
async def create_subject(
    subject: SubjectCreate,
    db=Depends(get_db),
    current_user: User = Depends(
        require_roles(UserRole.PROFESSOR, UserRole.ADMIN)
    ),
):
    # 중복 확인
    existing = db.query(Subject).filter(Subject.name == subject.name).first()
    if existing:
        raise HTTPException(status_code=400, detail="Subject already exists")
    
    db_subject = Subject(name=subject.name, description=subject.description)
    db.add(db_subject)
    db.commit()
    db.refresh(db_subject)
    return db_subject

# 과목 수정
@router.put("/{subject_id}", response_model=SubjectResponse)
async def update_subject(
    subject_id: int,
    subject_update: SubjectUpdate,
    db=Depends(get_db),
    current_user: User = Depends(
        require_roles(UserRole.PROFESSOR, UserRole.ADMIN)
    ),
):
    db_subject = db.query(Subject).filter(Subject.id == subject_id).first()
    if not db_subject:
        raise HTTPException(status_code=404, detail="Subject not found")
    
    update_data = subject_update.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_subject, key, value)
    
    db.commit()
    db.refresh(db_subject)
    return db_subject

# 과목 삭제
@router.delete("/{subject_id}")
async def delete_subject(
    subject_id: int,
    db=Depends(get_db),
    current_user: User = Depends(require_roles(UserRole.ADMIN)),
):
    db_subject = db.query(Subject).filter(Subject.id == subject_id).first()
    if not db_subject:
        raise HTTPException(status_code=404, detail="Subject not found")
    
    db.delete(db_subject)
    db.commit()
    return {"message": "Subject deleted successfully"}
