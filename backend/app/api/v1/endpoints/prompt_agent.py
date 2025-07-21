from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel
from app.services.articles import generate_and_publish
from app.api.deps import get_db, get_current_user
from app.schemas.article import Article

router = APIRouter()

class PromptRequest(BaseModel):
    prompt: str

@router.post("/", response_model=Article, status_code=status.HTTP_201_CREATED)
async def prompt_agent(req: PromptRequest, db: AsyncSession = Depends(get_db), current_user=Depends(get_current_user)):
    return await generate_and_publish(db, req.prompt, current_user)
