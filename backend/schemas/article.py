from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, ConfigDict, model_validator


# ---------- schemat wejściowy – ręczne tworzenie ----------
class ArticleCreate(BaseModel):
    title:            str = Field(..., max_length=200)
    content:          str
    meta_description: Optional[str] = Field(None, max_length=300)
    image_prompt:     Optional[str] = None


# ---------- wejściowy – AI‑generator ----------
class ArticleGenerateRequest(BaseModel):
    topic: str = Field(..., min_length=5, max_length=150)


# ---------- częściowa aktualizacja ----------
class ArticleUpdate(BaseModel):
    title:   Optional[str] = None
    content: Optional[str] = None

    # v2 – walidator AFTER; sprawdza, że coś faktycznie przyszło
    @model_validator(mode="after")
    def _at_least_one_field(cls, values):
        if not (values.title or values.content):
            raise ValueError("Provide at least one field to update")
        return values


# ---------- schemat wyjściowy ----------
class ArticleOut(BaseModel):
    id:              int
    title:           str
    content:         str
    meta_description:Optional[str]
    image_prompt:    Optional[str]
    image_url:       Optional[str]
    wordpress_id:    Optional[int]
    wordpress_url:   Optional[str]
    published_at:    Optional[datetime]
    twitter_posted_at:   Optional[datetime]
    instagram_posted_at: Optional[datetime]
    created_at:      datetime

    # **tylko jedna** konfiguracja v2
    model_config = ConfigDict(
        from_attributes=True,                 # zastępuje orm_mode=True
        json_encoders={datetime: lambda d: d.isoformat()},
    )
