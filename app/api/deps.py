from fastapi import Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from jose import JWTError, jwt

from app.db.session import get_session
from app.core.config import get_settings
from app.models.user import User
from sqlalchemy import select

settings = get_settings()

async def get_db():
    async for session in get_session():
        yield session

def get_current_user(token: str = Depends(lambda: None), db: AsyncSession = Depends(get_db)) -> User:
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate credentials")
    if token is None:
        raise credentials_exception
    try:
        payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
        email: str = payload.get("sub")
    except JWTError:
        raise credentials_exception
    if email is None:
        raise credentials_exception
    user = (await db.execute(select(User).where(User.email == email))).scalars().first()
    if user is None:
        raise credentials_exception
    return user
