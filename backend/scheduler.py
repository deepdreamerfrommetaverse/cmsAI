"""
Scheduler – zadania w tle.

• run_scheduler          – Twoja pierwotna funkcja (publikuje najstarszy draft
                           lub generuje/publikuje, gdy brak).
• start_article_scheduler – NOWA pętla generująca & publikująca
                           „fresh finance article” co N h.
• stop_scheduler         – hook wywoływany z main.py (rozszerzalny).
"""

import asyncio
import logging
from datetime import datetime
from sqlalchemy.orm import Session

from database import SessionLocal
from core.settings import settings
from services import article_service

logger = logging.getLogger(__name__)

# ----------------------------------------------------------------------
async def run_scheduler():
    """
    Publikuje co N h najstarszy nieopublikowany artykuł,
    a gdy brak – generuje nowy i publikuje. (Twoja oryginalna logika)
    """
    interval = settings.article_publish_interval  # hours
    while True:
        await asyncio.sleep(interval * 3600)
        try:
            db: Session = SessionLocal()
            try:
                article = (
                    db.query(article_service.ArticleModel)
                    .filter_by(published_at=None)
                    .order_by(article_service.ArticleModel.created_at)
                    .first()
                )
                if article:
                    logger.info("Scheduler publishing draft ID=%s", article.id)
                    article_service.publish_article(db, article)
                else:
                    if settings.openai_api_key:
                        logger.info("No drafts – generating new article via AI.")
                        new_article = article_service.generate_article(db)
                        article_service.publish_article(db, new_article)
                    else:
                        logger.info("No drafts and OpenAI disabled – skipping.")
            finally:
                db.close()
        except Exception as exc:
            logger.error("run_scheduler error: %s", exc)

# ----------------------------------------------------------------------
async def start_article_scheduler(app):
    """
    Generuje **zawsze nowy** artykuł (topic='fresh finance article')
    co N h i publikuje go od razu. Działa równolegle z run_scheduler.
    """
    interval = settings.article_publish_interval
    logger.info("Article‑generator scheduler started (every %dh).", interval)
    while True:
        await asyncio.sleep(interval * 3600)
        db: Session = SessionLocal()
        try:
            article = article_service.generate_article(db, topic="fresh finance article")
            article_service.publish_article(db, article)
            logger.info("Auto‑generated & published article ID=%s", article.id)
        except Exception as exc:
            logger.error("start_article_scheduler error: %s", exc)
        finally:
            db.close()

# ----------------------------------------------------------------------
async def stop_scheduler():
    """
    Placeholder na dodatkowe clean‑up’y (np. APScheduler).
    Obecnie loguje tylko informację – rozszerzalne przy kolejnych zadaniach.
    """
    logger.info("stop_scheduler hook executed at %s", datetime.utcnow().isoformat())
