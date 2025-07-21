from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.user import User
from app.schemas.user import UserCreate
from app.core.security import get_password_hash, verify_password, create_access_token

async def create_user(db: AsyncSession, user_in: UserCreate) -> User:
    user = User(email=user_in.email, hashed_password=get_password_hash(user_in.password))
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user

async def authenticate(db: AsyncSession, email: str, password: str) -> str | None:
    q = await db.execute(select(User).where(User.email == email))
    user = q.scalars().first()
    if not user or not verify_password(password, user.hashed_password):
        return None
    token = create_access_token({"sub": user.email})
    return token
