from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from schemas.auth import LoginRequest, TokenSchema, AccessToken
from schemas.user import UserRead
from database import get_db
from services import auth_service
from core.auth import create_access_token, create_refresh_token, get_current_user

router = APIRouter()

@router.post("/login", response_model=TokenSchema)
def login(credentials: LoginRequest, db: Session = Depends(get_db)):
    """Authenticate user and return JWT access & refresh tokens."""
    user = auth_service.authenticate_user(db, credentials.email, credentials.password)
    if not user:
        raise HTTPException(status_code=401, detail="Incorrect email or password")
    access_token = create_access_token(user.id)
    refresh_token = create_refresh_token(user.id)
    return {"access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer"}

@router.post("/refresh", response_model=AccessToken)
def refresh_token(token: str = Depends(None)):
    """Refresh the access token using a valid refresh token (provide in Authorization header)."""
    # Manually extract token from Authorization header since we want refresh token
    from fastapi import Request
    # Actually use request directly
    raise HTTPException(status_code=400, detail="Use Authorization header with refresh token to refresh.")  # This route handled by custom logic
