from datetime import datetime
from sqlalchemy import Column, Integer, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class Version(Base):
    __tablename__ = "versions"

    id          = Column(Integer, primary_key=True)
    article_id  = Column(Integer, ForeignKey("articles.id", ondelete="CASCADE"))
    diff        = Column(Text, nullable=False)
    created_at  = Column(DateTime, default=datetime.utcnow, nullable=False)

    article     = relationship("Article", back_populates="versions")
