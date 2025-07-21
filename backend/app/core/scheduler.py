import logging
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger
from contextlib import asynccontextmanager

log = logging.getLogger(__name__)
scheduler: AsyncIOScheduler | None = None

def _schedule_jobs():
    from app.core.ai_client import generate_article  # lazy import
    from app.services.articles import create_article
    from app.db.session import get_session
    from app.schemas.article import ArticleCreate

    async def publish_fresh_article():
        prompt = "Napisz świeży artykuł finansowy (500 słów, wypunktowania, wnioski)."
        article_body = await generate_article(prompt)
        art_in = ArticleCreate(
            title="Auto article",
            slug="auto-" + str(abs(hash(article_body)) % 10000),
            body=article_body
        )
        async for db in get_session():
            await create_article(db, art_in, author_id=1)
        log.info("Auto article published")

    scheduler.add_job(publish_fresh_article, IntervalTrigger(hours=6), id="auto_article")

def start():
    global scheduler
    if scheduler is None:
        scheduler = AsyncIOScheduler()
        _schedule_jobs()
        scheduler.start()
        log.info("APScheduler started")

async def shutdown():
    global scheduler
    if scheduler:
        await scheduler.shutdown()
        log.info("APScheduler stopped")
        scheduler = None
