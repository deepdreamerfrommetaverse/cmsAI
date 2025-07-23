from sqlalchemy import func
from sqlalchemy.orm import Session

from models.analytics import AnalyticsEvent

def track_event(db: Session, event_type: str, event_data_str: str = None):
    """Record a new analytics event in the database."""
    event = AnalyticsEvent(event_type=event_type, event_data=event_data_str)
    db.add(event)
    db.commit()
    return event

def get_summary(db: Session):
    """Compute analytics summary: total events, page views count, and counts by event type."""
    total = db.query(func.count(AnalyticsEvent.id)).scalar() or 0
    result = db.query(AnalyticsEvent.event_type, func.count(AnalyticsEvent.id)).group_by(AnalyticsEvent.event_type).all()
    breakdown = {etype: count for etype, count in result}
    page_views = breakdown.get("page_view", 0)
    return {"total_events": int(total), "page_views": int(page_views), "events_by_type": {k: int(v) for k, v in breakdown.items()}}
