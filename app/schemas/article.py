from typing import Optional
from pydantic import BaseModel

class ArticleBase(BaseModel):
    title: str
    slug: str
    body: str
    hero_url: Optional[str] = None

class ArticleCreate(ArticleBase):
    pass

class Article(ArticleBase):
    id: int
    wp_post_id: Optional[int] = None
    author_id: int

    class Config:
        orm_mode = True
