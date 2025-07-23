from typing import Optional
from pydantic import BaseModel

class ArticleCreate(BaseModel):
    title: str
    content: str
    meta_description: Optional[str] = None
    image_prompt: Optional[str] = None

class ArticleGenerateRequest(BaseModel):
    topic: Optional[str] = None

class ArticleUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None

    # Ensure at least one field is provided
    @classmethod
    def validate(cls, values):
        if not values.get('title') and not values.get('content'):
            raise ValueError("No new data provided for update")
        return values

class ArticleOut(BaseModel):
    id: int
    title: str
    content: str
    meta_description: Optional[str]
    image_prompt: Optional[str]
    image_url: Optional[str]
    wordpress_id: Optional[int]
    wordpress_url: Optional[str]
    published_at: Optional[str]
    twitter_posted_at: Optional[str]
    instagram_posted_at: Optional[str]
    created_at: str

    class Config:
        orm_mode = True
