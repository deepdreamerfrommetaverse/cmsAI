from datetime import datetime, timedelta
from typing import Optional

import jwt
from fastapi import HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext

from core.settings import settings

# JWT OAuth2 scheme for extracting tokens from Authorization header
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

# Password hashing context (using bcrypt)
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a plaintext password against the hashed password."""
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    """Hash a plaintext password."""
    return pwd_context.hash(password)

def create_access_token(user_id: int) -> str:
    """Generate a new JWT access token for the given user ID."""
    expire = datetime.utcnow() + timedelta(minutes=settings.access_token_expire_minutes)
    payload = {"user_id": user_id, "type": "access", "exp": expire}
    token = jwt.encode(payload, settings.secret_key, algorithm=settings.algorithm)
    return token

def create_refresh_token(user_id: int) -> str:
    """Generate a new JWT refresh token for the given user ID."""
    expire = datetime.utcnow() + timedelta(minutes=settings.refresh_token_expire_minutes)
    payload = {"user_id": user_id, "type": "refresh", "exp": expire}
    token = jwt.encode(payload, settings.secret_key, algorithm=settings.algorithm)
    return token

async def get_current_user(token: str = Depends(oauth2_scheme)):
    """Dependency to get the current logged-in User from JWT token."""
    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Could not validate credentials")
    user_id: Optional[int] = payload.get("user_id")
    token_type: Optional[str] = payload.get("type")
    if user_id is None or token_type != "access":
        raise HTTPException(status_code=401, detail="Could not validate credentials")
    # Retrieve user from database
    from models.user import User  # import here to avoid circular dependency
    from database import SessionLocal
    db = SessionLocal()
    try:
        user = db.query(User).get(user_id)
    finally:
        db.close()
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    return user

async def get_current_admin(current_user=Depends(get_current_user)):
    """Dependency to allow only admin users."""
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Admin privileges required")
    return current_user
