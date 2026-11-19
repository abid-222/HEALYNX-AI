from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker
from app.core.config import settings

_db_url = settings.normalized_database_url
_args = {"check_same_thread": False} if _db_url.startswith("sqlite") else {}
_pool = {} if _db_url.startswith("sqlite") else dict(pool_pre_ping=True, pool_size=5, max_overflow=5, pool_recycle=1800)  # small pool: Supabase poolers cap connections
engine = create_engine(_db_url, connect_args=_args, future=True, **_pool)
SessionLocal = sessionmaker(bind=engine, autoflush=False, expire_on_commit=False)


class Base(DeclarativeBase):
    pass


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
