from sqlalchemy import Column, Integer, String, DateTime, func
from app.db.session import Base

class AnalyticsEvent(Base):
    __tablename__ = "analytics_events"

    id = Column(Integer, primary_key=True, index=True)
    path = Column(String, nullable=False)
    event_type = Column(String, default="pageview")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
