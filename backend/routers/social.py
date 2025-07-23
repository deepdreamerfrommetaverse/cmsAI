"""
Router Social – publikowanie postów na Twitter / Instagram.

• chroniony dependencją get_current_admin,
• wymaga, by artykuł był już opublikowany (ma URL / image_url).
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from services import social_service, article_service
from core.auth import get_current_admin

router = APIRouter()

# ---------- POST /social/twitter/{article_id} ----------
@router.post("/twitter/{article_id}", status_code=204)
def tweet_article(
    article_id: int,
    db: Session = Depends(get_db),
    _admin=Depends(get_current_admin),
):
    article = db.query(article_service.ArticleModel).get(article_id)
    if not article or not article.wordpress_url:
        raise HTTPException(status_code=404, detail="Article not published")

    text = f"{article.title} {article.wordpress_url}"
    if len(text) > 256:
        text = text[:253] + "..."
    social_service.post_to_twitter(None, text)
    article.twitter_posted_at = article_service.datetime.utcnow()
    db.commit()
    return None


# ---------- POST /social/instagram/{article_id} ----------
@router.post("/instagram/{article_id}", status_code=204)
def post_instagram(
    article_id: int,
    db: Session = Depends(get_db),
    _admin=Depends(get_current_admin),
):
    article = db.query(article_service.ArticleModel).get(article_id)
    if not article or not article.image_url:
        raise HTTPException(status_code=404, detail="Hero image missing")

    caption = f"{article.title}\nRead more: {article.wordpress_url}"
    social_service.post_to_instagram(article.image_url, caption)
    article.instagram_posted_at = article_service.datetime.utcnow()
    db.commit()
    return None
