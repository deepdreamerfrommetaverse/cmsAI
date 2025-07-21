from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel
from app.services.social import tweet, ig_post, get_limits
from app.api.deps import get_db, get_current_user

router = APIRouter()

class TweetPayload(BaseModel):
    text: str
    media_url: str | None = None

@router.post("/tweet", status_code=status.HTTP_201_CREATED)
async def post_tweet(payload: TweetPayload, db: AsyncSession = Depends(get_db), current_user=Depends(get_current_user)):
    return await tweet(db, payload.text, payload.media_url)

class IgPayload(BaseModel):
    caption: str
    image_url: str

@router.post("/instagram", status_code=status.HTTP_201_CREATED)
async def post_ig(payload: IgPayload, db: AsyncSession = Depends(get_db), current_user=Depends(get_current_user)):
    return await ig_post(db, payload.caption, payload.image_url)

@router.get("/limits")
async def limits(db: AsyncSession = Depends(get_db), current_user=Depends(get_current_user)):
    return await get_limits(db)
