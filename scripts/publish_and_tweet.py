#!/usr/bin/env python3
"""
Simple script to publish the oldest draft article to WordPress and tweet it.
"""
import asyncio
from backend.services import article_service, wordpress_service, social_service
from backend.database import SessionLocal

async def main():
    db = SessionLocal()
    try:
        # Find oldest unpublished article
        article = db.query(article_service.ArticleModel).filter_by(published_at=None).order_by(article_service.ArticleModel.created_at).first()
        if not article:
            print("No unpublished draft articles found.")
            return
        if not wordpress_service.is_configured():
            print("WordPress integration not configured. Cannot publish.")
            return
        # Publish the article (this will also handle social media posting if configured)
        published = article_service.publish_article(db, article)
        print(f"Published article ID={published.id} to WordPress: {published.wordpress_url}")
    finally:
        db.close()

# Run the async main
asyncio.run(main())
