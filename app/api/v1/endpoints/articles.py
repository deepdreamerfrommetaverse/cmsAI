from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from app.schemas.article import Article, ArticleCreate
from app.services.articles import list_articles, create_article
from app.api.deps import get_db, get_current_user

router = APIRouter()

@router.get("/", response_model=List[Article])
async def articles(db: AsyncSession = Depends(get_db)):
    return await list_articles(db)

@router.post("/", response_model=Article, status_code=status.HTTP_201_CREATED)
async def new_article(article_in: ArticleCreate, db: AsyncSession = Depends(get_db), current_user=Depends(get_current_user)):
    return await create_article(db, article_in, author_id=current_user.id)
