from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime
from datetime import datetime
from database import Base                # OK – po fixie z pkt 1

from models import Base

class Feedback(Base):
    """Feedback model for user-submitted feedback or contact messages."""
    __tablename__ = "feedback"
    id = Column(Integer, primary_key=True)
    message = Column(Text, nullable=False)
    email = Column(String(255))
    name = Column(String(100))
    resolved = Column(Boolean, default=False, nullable=False)
    resolved_at = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
