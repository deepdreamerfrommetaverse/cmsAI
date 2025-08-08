# backend/database.py   ← upewnij się, że wygląda TAK

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from core.settings import settings

DB_URL = settings.database_url   # np. postgresql://user:pass@db:5432/ai_cms

engine = create_engine(DB_URL, pool_pre_ping=True)

# ← DODAJ TO
Base = declarative_base()        # <- potrzebne dla modeli i Alembica
# ↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# dependency dla FastAPI
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
