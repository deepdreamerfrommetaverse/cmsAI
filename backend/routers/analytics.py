from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from schemas.analytics import AnalyticsEventCreate, AnalyticsSummary
from database import get_db
from services import analytics_service
from core.auth import get_current_user

router = APIRouter()

@router.post("/track", status_code=204)
def track_event(event: AnalyticsEventCreate, db: Session = Depends(get_db)):
    """Track a page view or custom event (public)."""
    data_str = None
    if event.event_data is not None:
        # Convert event data to string if dict or other
        data_str = event.event_data if isinstance(event.event_data, str) else str(event.event_data)
    analytics_service.track_event(db, event.event_type, data_str)
    # Return no content
    return None

@router.get("/summary", response_model=AnalyticsSummary)
def analytics_summary(db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    """Get aggregate analytics summary (requires login)."""
    summary = analytics_service.get_summary(db)
    return summary
