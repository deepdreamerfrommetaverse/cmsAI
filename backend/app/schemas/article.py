from typing import Optional, List
from pydantic import BaseModel, Field

class ArticleBase(BaseModel):
    title: str
    slug: str
    body: str
    hero_url: Optional[str] = None
    meta_title: Optional[str] = Field(None, max_length=60)
    meta_description: Optional[str] = Field(None, max_length=155)
    keywords: Optional[str] = None
    layout_json: Optional[dict] = None

class ArticleCreate(ArticleBase):
    pass

class Article(ArticleBase):
    id: int
    wp_post_id: Optional[int] = None
    author_id: int

    class Config:
        orm_mode = True
