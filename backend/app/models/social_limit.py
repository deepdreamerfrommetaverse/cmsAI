from sqlalchemy import Column, Integer, String, Date, func, UniqueConstraint
from app.db.session import Base

class SocialLimit(Base):
    __tablename__ = "social_limits"
    id = Column(Integer, primary_key=True)
    service = Column(String, nullable=False)  # twitter / instagram
    date = Column(Date, server_default=func.current_date(), nullable=False)
    count = Column(Integer, default=0)
    limit = Column(Integer, nullable=False)

    __table_args__ = (UniqueConstraint('service', 'date', name='uix_service_date'), )
