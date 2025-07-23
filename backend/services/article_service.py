import difflib
import random
from datetime import datetime
from sqlalchemy.orm import Session

from core import openai_client
from models.article import Article
from models.version import Version

# Example topics for auto-generation if none provided
DEFAULT_TOPICS = [
    "the latest advancements in artificial intelligence",
    "sustainable energy solutions in modern cities",
    "the impact of blockchain on finance",
    "health benefits of meditation",
    "the future of space exploration",
    "cybersecurity trends in 2025",
    "the evolution of electric vehicles",
    "effective remote work strategies",
    "advancements in quantum computing",
    "the importance of mental health awareness"
]

# Expose Article model for external use (e.g., scheduler)
ArticleModel = Article

def generate_article(db: Session, topic: str = None):
    """Generate a new article (title, content, meta, image_prompt) using AI and save it to the database."""
    # Choose a random topic if none provided
    if not topic:
        topic = random.choice(DEFAULT_TOPICS)
    # Use OpenAI to generate article data
    result = openai_client.generate_article(topic)
    # Fallback handling if keys missing
    title = result.get("title") or topic.title()
    content = result.get("content") or ""
    meta_desc = result.get("meta_description")
    if not meta_desc:
        # If AI didn't provide meta, use first 155 characters of content as meta description
        meta_desc = content[:155]
    image_prompt = result.get("image_prompt")
    if not image_prompt:
        image_prompt = f"An illustration of {title}"
    # Create Article record
    article = Article(
        title=title,
        content=content,
        meta_description=meta_desc,
        image_prompt=image_prompt
    )
    db.add(article)
    db.commit()
    db.refresh(article)
    return article

def update_article(db: Session, article: Article, new_title: str, new_content: str):
    """Update an article's title/content and record the changes in version history."""
    old_title = article.title
    old_content = article.content
    # Compute diff of changes
    old_lines = [f"Title: {old_title}"] + old_content.splitlines()
    new_lines = [f"Title: {new_title if new_title is not None else old_title}"] + new_content.splitlines()
    diff_lines = difflib.unified_diff(old_lines, new_lines, fromfile="old", tofile="new", lineterm="")
    diff_text = "\n".join(diff_lines)
    # Only create version entry if there are changes
    if new_title is not None or new_content is not None:
        version = Version(article_id=article.id, diff=diff_text, created_at=datetime.utcnow())
        db.add(version)
    # Apply updates to article
    if new_title is not None:
        article.title = new_title
    if new_content is not None:
        article.content = new_content
    db.commit()
    db.refresh(article)
    return article

def publish_article(db: Session, article: Article):
    """Publish an article to WordPress and share on social platforms."""
    from services import wordpress_service, social_service
    if article.published_at:
        raise HTTPException(status_code=400, detail="Article is already published")
    # Ensure WordPress integration is configured
    if not (wordpress_service.is_configured()):
        raise HTTPException(status_code=503, detail="WordPress integration not configured")
    # Generate hero image via OpenAI (if prompt available)
    image_bytes = None
    image_type = None
    image_ext = None
    try:
        prompt = article.image_prompt or f"An illustration of {article.title}"
        image_bytes, image_type, image_ext = openai_client.generate_image(prompt)
    except Exception as e:
        # Log image generation failure and continue without image
        msg = str(e)
        logging = __import__("logging")  # import logging lazily
        logging.getLogger(__name__).warning(f"Image generation failed: {msg}. Publishing without image.")
        image_bytes = None
    # Publish to WordPress
    wp_id, wp_link, media_url = wordpress_service.publish_to_wordpress(article, image_bytes, image_type, image_ext)
    # Update article with WordPress info
    article.wordpress_id = wp_id
    article.wordpress_url = wp_link
    article.image_url = media_url
    article.published_at = datetime.utcnow()
    db.commit()
    # Social sharing
    now = datetime.utcnow()
    # Twitter/X share
    if social_service.is_twitter_configured():
        # Check daily limit for Twitter posts
        tweets_last_24h = db.query(Article).filter(Article.twitter_posted_at != None, Article.twitter_posted_at >= (now - timedelta(days=1))).count()
        if tweets_last_24h < social_service.MAX_TWITTER_POSTS_PER_DAY:
            try:
                text = f"{article.title} {article.wordpress_url}"
                if len(text) > 256:
                    text = text[:253] + "..."
                    text += " " + article.wordpress_url
                if image_bytes:
                    social_service.post_to_twitter(image_bytes, text)
                else:
                    social_service.post_to_twitter(None, text)
                article.twitter_posted_at = datetime.utcnow()
            except Exception as e:
                logging.getLogger(__name__).error(f"Twitter post failed: {e}")
        else:
            logging.getLogger(__name__).warning("Daily Twitter post limit reached, skipping Twitter share.")
    # Instagram share
    if social_service.is_instagram_configured() and article.image_url:
        ig_posts_last_24h = db.query(Article).filter(Article.instagram_posted_at != None, Article.instagram_posted_at >= (now - timedelta(days=1))).count()
        if ig_posts_last_24h < social_service.MAX_IG_POSTS_PER_DAY:
            try:
                caption = f"{article.title}\nRead more on {article.wordpress_url.split('//')[-1].split('/')[0]}."
                social_service.post_to_instagram(article.image_url, caption)
                article.instagram_posted_at = datetime.utcnow()
            except Exception as e:
                logging.getLogger(__name__).error(f"Instagram post failed: {e}")
        else:
            logging.getLogger(__name__).warning("Daily Instagram post limit reached, skipping Instagram share.")
    # Save social timestamps
    db.commit()
    db.refresh(article)
    return article
