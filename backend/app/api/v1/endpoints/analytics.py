from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel
from app.services.analytics import track_event, get_stats
from app.services.stripe import get_revenue
from app.api.deps import get_db

router = APIRouter()

class TrackPayload(BaseModel):
    path: str
    event_type: str = "pageview"

@router.post("/track", status_code=status.HTTP_204_NO_CONTENT)
async def track(p: TrackPayload, db: AsyncSession = Depends(get_db)):
    await track_event(db, p.path, p.event_type)

@router.get("/stats")
async def stats(db: AsyncSession = Depends(get_db)):
    return await get_stats(db)

@router.get("/stripe/revenue")
async def stripe_revenue():
    return await get_revenue()
