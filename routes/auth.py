from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from config import settings
from models import User, UserRole, get_db
from schemas.auth import (
    LoginRequest,
    RegisterRequest,
    TokenResponse,
    UserResponse,
    UserUpdateRequest,
)
from services.auth import (
    create_access_token,
    get_current_user,
    hash_password,
    verify_password,
)

router = APIRouter()


@router.post("/register", response_model=TokenResponse, status_code=201)
async def register(payload: RegisterRequest, db: Session = Depends(get_db)):
    email = payload.email.lower().strip()
    if db.query(User).filter(User.email == email).first():
        raise HTTPException(status_code=409, detail="이미 가입된 이메일입니다.")
    if payload.role == UserRole.ADMIN and (
        not settings.ADMIN_SIGNUP_CODE
        or payload.admin_signup_code != settings.ADMIN_SIGNUP_CODE
    ):
        raise HTTPException(status_code=403, detail="admin 가입 코드가 올바르지 않습니다.")

    user = User(
        name=payload.name.strip(),
        phone=payload.phone.strip(),
        email=email,
        password_hash=hash_password(payload.password),
        role=payload.role,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return {"access_token": create_access_token(user), "user": user}


@router.post("/login", response_model=TokenResponse)
async def login(payload: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == payload.email.lower().strip()).first()
    if user is None or not verify_password(payload.password, user.password_hash):
        raise HTTPException(status_code=401, detail="이메일 또는 비밀번호가 올바르지 않습니다.")
    return {"access_token": create_access_token(user), "user": user}


@router.get("/me", response_model=UserResponse)
async def me(current_user: User = Depends(get_current_user)):
    return current_user


@router.put("/me", response_model=UserResponse)
async def update_me(
    payload: UserUpdateRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    if payload.email is not None:
        email = payload.email.lower().strip()
        duplicate = (
            db.query(User)
            .filter(User.email == email, User.id != current_user.id)
            .first()
        )
        if duplicate:
            raise HTTPException(status_code=409, detail="이미 가입된 이메일입니다.")
        current_user.email = email

    if payload.name is not None:
        current_user.name = payload.name.strip()
    if payload.phone is not None:
        current_user.phone = payload.phone.strip()

    if payload.new_password is not None:
        if not payload.current_password or not verify_password(
            payload.current_password, current_user.password_hash
        ):
            raise HTTPException(status_code=400, detail="현재 비밀번호가 올바르지 않습니다.")
        current_user.password_hash = hash_password(payload.new_password)

    db.commit()
    db.refresh(current_user)
    return current_user
