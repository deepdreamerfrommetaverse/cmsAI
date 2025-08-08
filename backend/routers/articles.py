from __future__ import annotations

import re
from datetime import datetime
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette.responses import Response

from core.auth import get_current_admin, get_current_user
from database import get_db
from schemas.article import (
    ArticleCreate,
    ArticleGenerateRequest,
    ArticleOut,
    ArticleUpdate,
)
from services import article_service

router = APIRouter()
Article = article_service.ArticleModel  # dla czytelności


# ----------  helpers  -------------------------------------------------
def _pdf_filename(title: str, art_id: int) -> str:
    slug = re.sub(r"[^0-9a-zA-Z_-]", "_", title).lower() or f"article_{art_id}"
    return f"{slug[:50]}.pdf"


# ----------  CRUD  ----------------------------------------------------
@router.get("/", response_model=List[ArticleOut])
def list_articles(
    published: Optional[bool] = None,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    q = db.query(Article).order_by(Article.created_at.desc())
    if published is True:
        q = q.filter(Article.published_at.isnot(None))
    elif published is False:
        q = q.filter(Article.published_at.is_(None))
    return q.all()


@router.get("/{article_id}", response_model=ArticleOut)
def get_article(
    article_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    art = db.query(Article).get(article_id)
    if not art:
        raise HTTPException(404, "Article not found")
    return art


@router.post("/", response_model=ArticleOut)
def create_article(
    data: ArticleCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    art = Article(**data.dict())
    db.add(art)
    db.commit()
    db.refresh(art)
    return art


@router.post("/generate", response_model=ArticleOut)
def generate_article(
    req: ArticleGenerateRequest,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    return article_service.create_article(db, req.topic)


@router.put("/{article_id}", response_model=ArticleOut)
def update_article(
    article_id: int,
    data: ArticleUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    art = db.query(Article).get(article_id)
    if not art:
        raise HTTPException(404, "Article not found")
    return article_service.update_article(
        db,
        art,
        data.title or art.title,
        data.content or art.content,
    )


@router.delete("/{article_id}", status_code=204)
def delete_article(
    article_id: int,
    db: Session = Depends(get_db),
    current_admin=Depends(get_current_admin),
):
    art = db.query(Article).get(article_id)
    if not art:
        raise HTTPException(404, "Article not found")
    db.delete(art)
    db.commit()
    return None


# ----------  actions  -------------------------------------------------
@router.post("/{article_id}/publish", response_model=ArticleOut)
def publish_article(
    article_id: int,
    db: Session = Depends(get_db),
    current_admin=Depends(get_current_admin),
):
    art = db.query(Article).get(article_id)
    if not art:
        raise HTTPException(404, "Article not found")
    return article_service.publish_article(db, art)


@router.get("/{article_id}/versions", response_model=List[dict])
def versions(
    article_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    art = db.query(Article).get(article_id)
    if not art:
        raise HTTPException(404, "Article not found")
    return [
        {
            "id": v.id,
            "created_at": v.created_at.isoformat(),
            "diff": v.diff,
        }
        for v in sorted(art.versions, key=lambda x: x.created_at, reverse=True)
    ]


@router.get("/{article_id}/export/pdf")
def export_pdf(
    article_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    art = db.query(Article).get(article_id)
    if not art:
        raise HTTPException(404, "Article not found")

    html = (
        f"<html><head><meta charset='UTF-8'><title>{art.title}</title></head><body>"
        f"<h1>{art.title}</h1><div>{art.content}</div></body></html>"
    )
    from weasyprint import HTML

    pdf_bytes = HTML(string=html).write_pdf()
    return Response(
        pdf_bytes,
        media_type="application/pdf",
        headers={"Content-Disposition": f"attachment; filename={_pdf_filename(art.title, art.id)}"},
    )
