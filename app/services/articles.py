from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.article import Article
from app.schemas.article import ArticleCreate

async def list_articles(db: AsyncSession):
    res = await db.execute(select(Article))
    return res.scalars().all()

async def create_article(db: AsyncSession, article_in: ArticleCreate, author_id: int):
    article = Article(**article_in.dict(), author_id=author_id)
    db.add(article)
    await db.commit()
    await db.refresh(article)
    return article
