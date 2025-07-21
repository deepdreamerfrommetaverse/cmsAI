from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from app.schemas.feedback import FeedbackCreate, Feedback
from app.models.feedback import Feedback as FeedbackModel
from app.api.deps import get_db

router = APIRouter()

@router.post("/", response_model=Feedback, status_code=status.HTTP_201_CREATED)
async def add_feedback(payload: FeedbackCreate, db: AsyncSession = Depends(get_db)):
    fb = FeedbackModel(**payload.dict())
    db.add(fb)
    await db.commit()
    await db.refresh(fb)
    return fb

@router.get("/", response_model=List[Feedback])
async def list_feedback(db: AsyncSession = Depends(get_db)):
    res = await db.execute(FeedbackModel.__table__.select())
    return res.mappings().all()
