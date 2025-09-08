# api/src/db/session.py
from sqlmodel import SQLModel, create_engine, Session
from src.core.config import settings

engine = create_engine(settings.DATABASE_URL, echo=False)

def get_session():
    session = Session(engine)
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()
