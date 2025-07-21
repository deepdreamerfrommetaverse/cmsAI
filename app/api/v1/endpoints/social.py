from fastapi import APIRouter
from app.services.social import tweet

router = APIRouter()

@router.post("/tweet")
async def post_tweet(text: str):
    return await tweet(text)
