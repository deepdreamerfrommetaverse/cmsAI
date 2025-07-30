"""
Jedyny, oficjalny moduł odpowiedzialny za:
• haszowanie haseł (bcrypt)
• generowanie / weryfikację JWT (access & refresh)
• zależności FastAPI get_current_user / get_current_admin
"""

from datetime import datetime, timedelta
from typing import Optional

import jwt
from fastapi import HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext

from core.settings import settings


# ──────────────────────────────────────────────
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
ALGO = settings.algorithm
KEY  = settings.secret_key


# ─────────── helpers ───────────
def verify_password(plain: str, hashed: str) -> bool:
    return pwd_context.verify(plain, hashed)


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def _encode(payload: dict) -> str:
    return jwt.encode(payload, KEY, algorithm=ALGO)


def create_access_token(user_id: int) -> str:
    exp = datetime.utcnow() + timedelta(minutes=settings.access_token_expire_minutes)
    return _encode({"user_id": user_id, "type": "access", "exp": exp})


def create_refresh_token(user_id: int) -> str:
    exp = datetime.utcnow() + timedelta(minutes=settings.refresh_token_expire_minutes)
    return _encode({"user_id": user_id, "type": "refresh", "exp": exp})


def verify_refresh_token(token: str) -> int:
    try:
        payload = jwt.decode(token, KEY, algorithms=[ALGO])
    except jwt.ExpiredSignatureError:
        raise HTTPException(401, "Refresh token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(401, "Invalid refresh token")

    if payload.get("type") != "refresh":
        raise HTTPException(401, "Wrong token type")

    return payload["user_id"]


# ─────────── dependencies ───────────
async def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, KEY, algorithms=[ALGO])
    except jwt.ExpiredSignatureError:
        raise HTTPException(401, "Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(401, "Invalid token")

    if payload.get("type") != "access":
        raise HTTPException(401, "Wrong token type")

    # pobranie użytkownika
    from database import SessionLocal
    from models.user import User

    db = SessionLocal()
    try:
        user = db.query(User).get(payload["user_id"])
    finally:
        db.close()

    if not user:
        raise HTTPException(401, "User not found")
    return user


async def get_current_admin(current_user=Depends(get_current_user)):
    if current_user.role != "admin":
        raise HTTPException(403, "Admin privileges required")
    return current_user
