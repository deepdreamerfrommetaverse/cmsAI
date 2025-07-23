from typing import Optional
from pydantic import BaseModel, EmailStr, constr

class FeedbackCreate(BaseModel):
    message: constr(min_length=1)
    email: Optional[EmailStr] = None
    name: Optional[str] = None

class FeedbackUpdate(BaseModel):
    resolved: bool

class FeedbackOut(BaseModel):
    id: int
    message: str
    email: Optional[str]
    name: Optional[str]
    resolved: bool
    resolved_at: Optional[str]
    created_at: str

    class Config:
        orm_mode = True
