from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from schemas.auth import LoginRequest, TokenSchema, AccessToken
from schemas.user import UserRead
from database import get_db
from services import auth_service
from core.auth import create_access_token, create_refresh_token, get_current_user
from models.user import User  # potrzebny do weryfikacji refresh tokenu

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
def refresh_token(request: Request, db: Session = Depends(get_db)):
    """Refresh the access token using a valid refresh token (provide in Authorization header)."""
    auth_header = request.headers.get("authorization")
    if not auth_header:
        raise HTTPException(status_code=400, detail="Refresh token not provided in headers")
    # Pobierz token z nagłówka (format: "Bearer <token>")
    token_value = auth_header.split(" ", 1)[1] if auth_header.lower().startswith("bearer ") else auth_header
    # Zweryfikuj JWT (typ refresh)
    import jwt
    try:
        payload = jwt.decode(token_value, auth_service.settings.secret_key, algorithms=[auth_service.settings.algorithm])
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Refresh token has expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid refresh token")
    if payload.get("type") != "refresh" or payload.get("user_id") is None:
        raise HTTPException(status_code=401, detail="Invalid refresh token")
    user_id = payload["user_id"]
    # Weryfikacja istnienia użytkownika (opcjonalna, ale zwiększa bezpieczeństwo)
    user = db.query(User).get(user_id)
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    # Generuj nowy token dostępu
    new_access = create_access_token(user_id)
    return {"access_token": new_access, "token_type": "bearer"}

# (pozostałe endpointy bez zmian)

