from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from core.settings import settings

# Create SQLAlchemy engine and session factory
connect_args = {}
if settings.database_url.startswith("sqlite"):
    connect_args["check_same_thread"] = False  # needed for SQLite in multithreaded environment
engine = create_engine(settings.database_url, connect_args=connect_args, future=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False, expire_on_commit=False)

def get_db():
    """Dependency to provide a session per request."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
