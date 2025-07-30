from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session

from database import get_db
from models.user import User
from schemas.auth import LoginRequest, TokenSchema, AccessToken
from core.auth import (
    verify_password,
    create_access_token,
    create_refresh_token,
    verify_refresh_token,
)

router = APIRouter()        #  <-- bez prefixu!


# ─────────── LOGIN ───────────
@router.post("/login", response_model=TokenSchema)
def login(credentials: LoginRequest, db: Session = Depends(get_db)) -> TokenSchema:
    user = db.query(User).filter(User.email == credentials.email).first()
    if not user or not verify_password(credentials.password, user.hashed_password):
        raise HTTPException(401, "Invalid credentials")

    return {
        "access_token":  create_access_token(user.id),
        "refresh_token": create_refresh_token(user.id),
        "token_type":    "bearer",
    }


# ─────────── REFRESH ───────────
@router.post("/refresh", response_model=AccessToken)
def refresh_token(request: Request, db: Session = Depends(get_db)) -> AccessToken:
    auth = request.headers.get("authorization", "")
    if not auth.lower().startswith("bearer "):
        raise HTTPException(400, "Refresh token missing")

    refresh = auth.split(" ", 1)[1]
    user_id = verify_refresh_token(refresh)

    # (opcjonalnie) sprawdź czy user nadal istnieje
    if not db.query(User).get(user_id):
        raise HTTPException(401, "User not found")

    return {"access_token": create_access_token(user_id), "token_type": "bearer"}
