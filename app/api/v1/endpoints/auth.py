from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.user import UserCreate, User
from app.schemas.auth import LoginPayload, Token
from app.services.auth import create_user, authenticate
from app.api.deps import get_db

router = APIRouter()

@router.post("/register", response_model=User)
async def register(user_in: UserCreate, db: AsyncSession = Depends(get_db)):
    return await create_user(db, user_in)

@router.post("/login", response_model=Token)
async def login(payload: LoginPayload, db: AsyncSession = Depends(get_db)):
    token = await authenticate(db, payload.email, payload.password)
    if not token:
        raise HTTPException(status_code=400, detail="Incorrect credentials")
    return Token(access_token=token)
