import re
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from schemas.article import ArticleCreate, ArticleGenerateRequest, ArticleUpdate, ArticleOut
from database import get_db
from services import article_service
from core.auth import get_current_user, get_current_admin

router = APIRouter()

@router.get("/", response_model=list[ArticleOut])
def list_articles(published: bool = None, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    """List all articles. Optionally filter by published status."""
    query = db.query(article_service.ArticleModel)
    if published is True:
        query = query.filter(article_service.ArticleModel.published_at.isnot(None))
    elif published is False:
        query = query.filter(article_service.ArticleModel.published_at.is_(None))
    articles = query.order_by(article_service.ArticleModel.created_at.desc()).all()
    return articles

@router.get("/{article_id}", response_model=ArticleOut)
def get_article(article_id: int, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    """Retrieve a specific article by ID."""
    article = db.query(article_service.ArticleModel).get(article_id)
    if not article:
        raise HTTPException(status_code=404, detail="Article not found")
    return article

@router.post("/", response_model=ArticleOut)
def create_article(article_in: ArticleCreate, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    """Create a new article (manual content)."""
    meta_desc = article_in.meta_description
    if not meta_desc:
        # Derive a simple meta description if not provided
        meta_desc = (article_in.content[:155] or "")
    image_prompt = article_in.image_prompt
    new_article = article_service.ArticleModel(
        title=article_in.title,
        content=article_in.content,
        meta_description=meta_desc,
        image_prompt=image_prompt
    )
    db.add(new_article)
    db.commit()
    db.refresh(new_article)
    return new_article

@router.post("/generate", response_model=ArticleOut)
def generate_article(request: ArticleGenerateRequest, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    """Generate a new article using AI (OpenAI)."""
    topic = request.topic
    generated = article_service.generate_article(db, topic)
    return generated

@router.put("/{article_id}", response_model=ArticleOut)
def update_article(article_id: int, update: ArticleUpdate, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    """Update an existing article's title or content (creates a new version)."""
    article = db.query(article_service.ArticleModel).get(article_id)
    if not article:
        raise HTTPException(status_code=404, detail="Article not found")
    updated_article = article_service.update_article(db, article, update.title if update.title is not None else article.title, update.content if update.content is not None else article.content)
    return updated_article

@router.delete("/{article_id}", status_code=204)
def delete_article(article_id: int, db: Session = Depends(get_db), current_admin=Depends(get_current_admin)):
    """Delete an article and its version history (admin only)."""
    article = db.query(article_service.ArticleModel).get(article_id)
    if not article:
        raise HTTPException(status_code=404, detail="Article not found")
    db.delete(article)
    db.commit()
    return None

@router.post("/{article_id}/publish", response_model=ArticleOut)
def publish_article(article_id: int, db: Session = Depends(get_db), current_admin=Depends(get_current_admin)):
    """Publish an article to WordPress and share on social media (admin only)."""
    article = db.query(article_service.ArticleModel).get(article_id)
    if not article:
        raise HTTPException(status_code=404, detail="Article not found")
    published_article = article_service.publish_article(db, article)
    return published_article

@router.get("/{article_id}/versions", response_model=list[dict])
def get_article_versions(article_id: int, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    """Get version history of an article."""
    article = db.query(article_service.ArticleModel).get(article_id)
    if not article:
        raise HTTPException(status_code=404, detail="Article not found")
    versions = article.versions
    # Return list of diffs with timestamps
    return [{"id": v.id, "created_at": v.created_at.isoformat(), "diff": v.diff} for v in sorted(versions, key=lambda x: x.created_at, reverse=True)]

@router.get("/{article_id}/export/pdf")
def export_article_pdf(article_id: int, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    """Export an article as PDF."""
    article = db.query(article_service.ArticleModel).get(article_id)
    if not article:
        raise HTTPException(status_code=404, detail="Article not found")
    # Build HTML content
    html_content = f"""
    <html>
      <head>
        <meta charset="utf-8">
        <title>{article.title}</title>
        <style>
          body {{ font-family: Arial, sans-serif; margin: 50px; }}
          h1 {{ font-size: 2em; margin-bottom: 0.5em; }}
          h2 {{ font-size: 1.5em; margin-top: 1em; }}
          p {{ line-height: 1.6; }}
        </style>
      </head>
      <body>
        <h1>{article.title}</h1>
        {article.content}
      </body>
    </html>
    """
    from weasyprint import HTML
    pdf_bytes = HTML(string=html_content).write_pdf()
    # Generate filename slug
    slug = re.sub(r'[^0-9a-zA-Z_-]', '_', article.title).lower()
    if not slug:
        slug = f"article_{article.id}"
    filename = slug[:50] + ".pdf"
    from starlette.responses import Response
    headers = {"Content-Disposition": f"attachment; filename={filename}"}
    return Response(content=pdf_bytes, media_type="application/pdf", headers=headers)
