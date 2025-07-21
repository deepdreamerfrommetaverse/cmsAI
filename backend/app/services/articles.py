from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.article import Article
from app.schemas.article import ArticleCreate
from app.core.ai_client import generate_prompt_agent
from app.core.wp_client import create_post_full
from app.models.user import User

async def list_articles(db: AsyncSession):
    res = await db.execute(select(Article))
    return res.scalars().all()

async def create_article(db: AsyncSession, article_in: ArticleCreate, author_id: int):
    article = Article(**article_in.dict(exclude_unset=True), author_id=author_id)
    db.add(article)
    await db.commit()
    await db.refresh(article)
    return article

async def generate_and_publish(db: AsyncSession, prompt: str, author: User):
    gen = await generate_prompt_agent(prompt)
    art_in = ArticleCreate(
        title=gen["title"],
        slug=gen["title"].lower().replace(" ", "-"),
        body=gen["body"],
        hero_url=gen["hero_url"],
        meta_title=gen["meta_title"],
        meta_description=gen["meta_description"],
        keywords=gen["keywords"],
        layout_json=gen["layout_json"],
    )
    article = await create_article(db, art_in, author_id=author.id)

    # publish to WP
    meta = {
        "yoast_title": gen["meta_title"],
        "yoast_meta_description": gen["meta_description"],
        "keywords": gen["keywords"]
    }
    wp_post = await create_post_full({
        "title": gen["title"],
        "slug": art_in.slug,
        "content": gen["body"],
        "meta": meta,
        "layout_json": gen["layout_json"],
        "hero_url": gen["hero_url"]
    })
    article.wp_post_id = wp_post["id"]
    await db.commit()
    await db.refresh(article)
    return article
