from sqlalchemy import Column, Integer, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime

from models import Base

class Version(Base):
    """Version history model: stores diff of article content changes."""
    __tablename__ = "versions"
    id = Column(Integer, primary_key=True)
    article_id = Column(Integer, ForeignKey("articles.id", ondelete="CASCADE"), nullable=False)
    diff = Column(Text, nullable=False)         # Unified diff text representing changes
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    # Relationship back to Article
    article = relationship("Article", back_populates="versions")
