"""
Logika artykułów:
• generowanie treści + obrazu (OpenAI)
• zapis JPG/PNG do /static
• wersjonowanie diff-ów
• publikacja do WordPressa + social
"""

from __future__ import annotations

import logging
import uuid
from datetime import datetime, timedelta
from difflib import unified_diff
from pathlib import Path
from typing import Tuple

import requests
from sqlalchemy.orm import Session

from core.settings import settings
from core.openai_client import (
    generate_article as _ai_generate_article,
    generate_image as _ai_generate_image,
)
from models.article import Article
ArticleModel = Article        # alias wymagany przez routers/articles.py

from models.version import Version

# (opcjonalne) zewnętrzne moduły – jeśli nie istnieją, funkcje poniżej zignorują publikację
try:
    from services import wordpress_service, social_service
except ImportError:  # repo nie ma jeszcze tych plików
    wordpress_service = social_service = None  # type: ignore


# ————————————————————————————————————
STATIC_ROOT = Path("static")
STATIC_ROOT.mkdir(exist_ok=True)
log = logging.getLogger(__name__)
# ————————————————————————————————————


# ----------  helpers  -------------------------------------------------
def _save_image(binary: bytes, ext: str) -> str:
    """Zapisuje plik w `/static` i zwraca ścieżkę URL (Nginx alias)."""
    fname = f"{uuid.uuid4().hex}.{ext}"
    path = STATIC_ROOT / fname
    path.write_bytes(binary)
    return f"/static/{fname}"


def _build_diff(old: str, new: str) -> str:
    return "".join(
        unified_diff(
            old.splitlines(keepends=True),
            new.splitlines(keepends=True),
            fromfile="old",
            tofile="new",
            lineterm="",
        )
    )


# ----------  główne API  ---------------------------------------------
def create_article(db: Session, topic: str) -> Article:
    """
    • generuje (OpenAI) treść + obraz,
    • przechowuje plik w /static,
    • zapisuje rekord w DB.
    """
    ai = _ai_generate_article(topic)  # title, content, meta_description, image_prompt
    img_b, _, ext = _ai_generate_image(ai["image_prompt"])
    image_url = _save_image(img_b, ext)

    art = Article(
        title=ai["title"],
        content=ai["content"],
        meta_description=ai["meta_description"],
        image_prompt=ai["image_prompt"],
        image_url=image_url,
    )
    db.add(art)
    db.commit()
    db.refresh(art)
    return art


def update_article(
    db: Session,
    art: Article,
    new_title: str,
    new_content: str,
) -> Article:
    """
    Aktualizuje artykuł **i** zapisuje diff do `t_versions`
    (przy zmianie contentu).
    """
    if art.content != new_content:
        ver = Version(
            article_id=art.id,
            diff=_build_diff(art.content, new_content),
        )
        db.add(ver)

    art.title = new_title
    art.content = new_content
    db.commit()
    db.refresh(art)
    return art


# ----------  publikacja  ---------------------------------------------
def _maybe_publish_to_wordpress(art: Article, img_path: Path) -> Tuple[int, str, str]:
    """
    Zwraca: (wp_post_id, wp_link, wp_image_url).
    Jeżeli WordPress nie jest skonfigurowany – zwraca same zera/puste str.
    """
    if not (wordpress_service and wordpress_service.is_configured()):
        log.warning("WordPress not skonfigurowany – pomijam publikację.")
        return 0, "", art.image_url or ""

    wp_id, wp_link, media_url = wordpress_service.publish_to_wordpress(
        art, img_path.read_bytes(), "image/jpeg", img_path.suffix.lstrip(".")
    )
    return wp_id, wp_link, media_url


def _maybe_share_to_social(db: Session, art: Article) -> None:
    if not social_service:
        return

    now = datetime.utcnow()

    # ----------  Twitter / X  ----------
    if social_service.is_twitter_configured():
        tweets24h = (
            db.query(Article)
            .filter(Article.twitter_posted_at.isnot(None))
            .filter(Article.twitter_posted_at >= now - timedelta(days=1))
            .count()
        )
        if tweets24h < social_service.MAX_TWITTER_POSTS_PER_DAY:
            try:
                social_service.post_to_twitter(None, f"{art.title} {art.wordpress_url}")
                art.twitter_posted_at = datetime.utcnow()
            except Exception as e:  # noqa: BLE001
                log.error("Twitter share failed: %s", e)

    # ----------  Instagram  ----------
    if (
        social_service.is_instagram_configured()
        and art.image_url
        and art.instagram_posted_at is None
    ):
        ig24h = (
            db.query(Article)
            .filter(Article.instagram_posted_at.isnot(None))
            .filter(Article.instagram_posted_at >= now - timedelta(days=1))
            .count()
        )
        if ig24h < social_service.MAX_IG_POSTS_PER_DAY:
            try:
                caption = f"{art.title}\n\nPełny wpis: {art.wordpress_url}"
                social_service.post_to_instagram(art.image_url, caption)
                art.instagram_posted_at = datetime.utcnow()
            except Exception as e:  # noqa: BLE001
                log.error("Instagram share failed: %s", e)


def publish_article(db: Session, art: Article) -> Article:
    """
    • upload featured image,
    • publikacja WordPress,
    • (opcjonalnie) share na X / Instagram,
    • aktualizacja pól w DB.
    """
    if art.published_at:
        raise ValueError("Article already published")

    img_path = STATIC_ROOT / Path(art.image_url).name
    wp_id, wp_link, media_url = _maybe_publish_to_wordpress(art, img_path)

    art.wordpress_id = wp_id or None
    art.wordpress_url = wp_link or None
    art.image_url = media_url or art.image_url
    art.published_at = datetime.utcnow()
    db.commit()

    _maybe_share_to_social(db, art)

    db.commit()
    db.refresh(art)
    return art
