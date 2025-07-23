from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from schemas.user import UserCreate, UserRead
from database import get_db
from services import auth_service
from core.auth import get_current_admin

router = APIRouter()

@router.get("/", response_model=list[UserRead])
def list_users(db: Session = Depends(get_db), current_admin=Depends(get_current_admin)):
    """Retrieve all users (admin only)."""
    users = db.query(auth_service.User).all()  # User model import via auth_service for simplicity
    return users

@router.post("/", response_model=UserRead)
def create_user(user_in: UserCreate, db: Session = Depends(get_db), current_admin=Depends(get_current_admin)):
    """Create a new user (admin only)."""
    user = auth_service.create_user(db, user_in.email, user_in.password, user_in.role)
    return user
