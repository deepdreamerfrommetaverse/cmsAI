from database import Base                # OK – po fixie z pkt 1
from sqlalchemy import Column, Integer, String, Text, DateTime
from datetime import datetime

from models import Base

class AnalyticsEvent(Base):
    """Analytics event model for page views and custom events."""
    __tablename__ = "analytics"
    id = Column(Integer, primary_key=True)
    event_type = Column(String(50), nullable=False)
    event_data = Column(Text)  # JSON string or info about the event
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
