from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from schemas.feedback import FeedbackCreate, FeedbackUpdate, FeedbackOut
from database import get_db
from services import feedback_service
from core.auth import get_current_admin

router = APIRouter()

@router.post("/", status_code=201)
def submit_feedback(feedback_in: FeedbackCreate, db: Session = Depends(get_db)):
    """Submit a new feedback message (public endpoint)."""
    feedback = feedback_service.create_feedback(db, feedback_in.message, feedback_in.email, feedback_in.name)
    return {"message": "Thank you for your feedback!"}

@router.get("/", response_model=list[FeedbackOut])
def list_feedback(resolved: bool = None, db: Session = Depends(get_db), current_admin=Depends(get_current_admin)):
    """List all feedback entries (admin only)."""
    query = db.query(feedback_service.Feedback) if hasattr(feedback_service, "Feedback") else db.query(feedback_service.feedback_service.Feedback)  # ensure model is accessible
    if resolved is True:
        query = query.filter_by(resolved=True)
    elif resolved is False:
        query = query.filter_by(resolved=False)
    feedback_list = query.order_by(feedback_service.Feedback.created_at.desc()).all()
    return feedback_list

@router.patch("/{feedback_id}", response_model=FeedbackOut)
def update_feedback(feedback_id: int, update: FeedbackUpdate, db: Session = Depends(get_db), current_admin=Depends(get_current_admin)):
    """Update feedback status (mark resolved or reopen) (admin only)."""
    feedback = db.query(feedback_service.Feedback).get(feedback_id)
    if not feedback:
        raise HTTPException(status_code=404, detail="Feedback not found")
    updated = feedback_service.resolve_feedback(db, feedback, update.resolved)
    return updated

@router.delete("/{feedback_id}", status_code=204)
def delete_feedback(feedback_id: int, db: Session = Depends(get_db), current_admin=Depends(get_current_admin)):
    """Delete a feedback entry (admin only)."""
    feedback = db.query(feedback_service.Feedback).get(feedback_id)
    if not feedback:
        raise HTTPException(status_code=404, detail="Feedback not found")
    db.delete(feedback)
    db.commit()
    return None
