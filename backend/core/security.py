# backend/core/security.py  ─── CAŁY plik ───
from datetime import datetime, timedelta
from typing import Any, Dict

import jwt
from passlib.context import CryptContext

from core.settings import settings   # secret_key, algorithm

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# ───────── helpers ─────────
def verify_password(plain: str, hashed: str) -> bool:
    return pwd_context.verify(plain, hashed)


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def _build_claims(user_id: int, minutes: int, typ: str) -> Dict[str, Any]:
    exp = datetime.utcnow() + timedelta(minutes=minutes)
    return {"user_id": user_id, "type": typ, "exp": exp}


def create_access_token(user_id: int) -> str:
    claims = _build_claims(user_id, settings.access_token_expire_minutes, "access")
    return jwt.encode(claims, settings.secret_key, algorithm=settings.algorithm)


def create_refresh_token(user_id: int) -> str:
    claims = _build_claims(user_id, settings.refresh_token_expire_minutes, "refresh")
    return jwt.encode(claims, settings.secret_key, algorithm=settings.algorithm)


def verify_refresh_token(token: str) -> int:
    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
        if payload.get("type") != "refresh":
            raise ValueError("Not refresh")
        return int(payload["user_id"])
    except Exception:
        raise   # przechwytywane w routerze; zwróci 401
