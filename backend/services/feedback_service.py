from datetime import datetime
from sqlalchemy.orm import Session

from models.feedback import Feedback

def create_feedback(db: Session, message: str, email: str = None, name: str = None):
    """Save a new feedback entry."""
    feedback = Feedback(message=message, email=email, name=name, resolved=False)
    db.add(feedback)
    db.commit()
    db.refresh(feedback)
    return feedback

def resolve_feedback(db: Session, feedback: Feedback, resolved: bool):
    """Mark a feedback as resolved or open."""
    if resolved:
        feedback.resolved = True
        feedback.resolved_at = datetime.utcnow()
    else:
        feedback.resolved = False
        feedback.resolved_at = None
    db.commit()
    db.refresh(feedback)
    return feedback
