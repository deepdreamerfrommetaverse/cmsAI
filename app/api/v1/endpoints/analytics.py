from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.services.analytics import get_stats
from app.api.deps import get_db

router = APIRouter()

@router.get("/stats")
async def stats(db: AsyncSession = Depends(get_db)):
    return await get_stats(db)
