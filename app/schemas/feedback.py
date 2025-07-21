from pydantic import BaseModel

class FeedbackCreate(BaseModel):
    message: str
    email: str | None = None

class Feedback(BaseModel):
    id: int
    message: str
    email: str | None = None
    resolved: bool

    class Config:
        orm_mode = True
