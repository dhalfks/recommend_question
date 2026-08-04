import base64
import hashlib
import hmac
import json
import os
from datetime import datetime, timedelta, timezone
from typing import Callable

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from config import settings
from models import User, UserRole, get_db

bearer_scheme = HTTPBearer(auto_error=False)


def hash_password(password: str) -> str:
    salt = os.urandom(16)
    iterations = 600_000
    digest = hashlib.pbkdf2_hmac("sha256", password.encode(), salt, iterations)
    return f"pbkdf2_sha256${iterations}${salt.hex()}${digest.hex()}"


def verify_password(password: str, encoded: str) -> bool:
    try:
        algorithm, iterations, salt, expected = encoded.split("$", 3)
        if algorithm != "pbkdf2_sha256":
            return False
        actual = hashlib.pbkdf2_hmac(
            "sha256", password.encode(), bytes.fromhex(salt), int(iterations)
        )
        return hmac.compare_digest(actual, bytes.fromhex(expected))
    except (ValueError, TypeError):
        return False


def _base64url(data: bytes) -> str:
    return base64.urlsafe_b64encode(data).rstrip(b"=").decode()


def _decode_base64url(value: str) -> bytes:
    return base64.urlsafe_b64decode(value + "=" * (-len(value) % 4))


def create_access_token(user: User) -> str:
    now = datetime.now(timezone.utc)
    header = {"alg": "HS256", "typ": "JWT"}
    payload = {
        "sub": str(user.id),
        "role": user.role.value,
        "iat": int(now.timestamp()),
        "exp": int(
            (now + timedelta(minutes=settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES)).timestamp()
        ),
    }
    encoded_header = _base64url(json.dumps(header, separators=(",", ":")).encode())
    encoded_payload = _base64url(json.dumps(payload, separators=(",", ":")).encode())
    message = f"{encoded_header}.{encoded_payload}".encode()
    signature = _base64url(
        hmac.new(settings.JWT_SECRET_KEY.encode(), message, hashlib.sha256).digest()
    )
    return f"{encoded_header}.{encoded_payload}.{signature}"


def decode_access_token(token: str) -> dict:
    try:
        header, payload, signature = token.split(".")
        message = f"{header}.{payload}".encode()
        expected = _base64url(
            hmac.new(settings.JWT_SECRET_KEY.encode(), message, hashlib.sha256).digest()
        )
        if not hmac.compare_digest(signature, expected):
            raise ValueError("invalid signature")
        data = json.loads(_decode_base64url(payload))
        if int(data["exp"]) < int(datetime.now(timezone.utc).timestamp()):
            raise ValueError("expired token")
        return data
    except (ValueError, KeyError, json.JSONDecodeError):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="유효하지 않거나 만료된 인증 토큰입니다.",
            headers={"WWW-Authenticate": "Bearer"},
        )


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
    db: Session = Depends(get_db),
) -> User:
    if credentials is None or credentials.scheme.lower() != "bearer":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="로그인이 필요합니다.",
            headers={"WWW-Authenticate": "Bearer"},
        )
    payload = decode_access_token(credentials.credentials)
    user = db.query(User).filter(User.id == int(payload["sub"])).first()
    if user is None:
        raise HTTPException(status_code=401, detail="사용자를 찾을 수 없습니다.")
    return user


def require_roles(*allowed_roles: UserRole) -> Callable:
    def dependency(current_user: User = Depends(get_current_user)) -> User:
        if current_user.role not in allowed_roles:
            raise HTTPException(status_code=403, detail="이 작업을 수행할 권한이 없습니다.")
        return current_user

    return dependency
