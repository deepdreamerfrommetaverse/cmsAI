from fastapi import HTTPException
from sqlalchemy.orm import Session

from core.auth import verify_password, get_password_hash
from models.user import User

def authenticate_user(db: Session, email: str, password: str):
    """Verify email and password, returning the user if valid or None if not."""
    user = db.query(User).filter(User.email == email).first()
    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user

def create_user(db: Session, email: str, password: str, role: str):
    """Create a new user with the given email, password, and role (admin/editor)."""
    # Check if email already exists
    existing = db.query(User).filter(User.email == email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email is already registered")
    # Only allow certain roles
    if role not in ("admin", "editor"):
        raise HTTPException(status_code=400, detail="Invalid user role")
    hashed_pw = get_password_hash(password)
    user = User(email=email, hashed_password=hashed_pw, role=role)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user
