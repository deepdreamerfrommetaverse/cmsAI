from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
from database import Base                # OK – po fixie z pkt 1

from models import Base

class User(Base):
    """User account model (admin/editor)."""
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), nullable=False, unique=True, index=True)
    hashed_password = Column(String(100), nullable=False)
    role = Column(String(50), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
