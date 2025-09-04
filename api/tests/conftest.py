# conftest.py
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from api.src import domain
from api.src.cruds.users import UsersRepository
from sqlmodel import SQLModel

@pytest.fixture(scope="session")
def engine():
    engine = create_engine("sqlite:///:memory:", echo=False, future=True)
    SQLModel.metadata.create_all(engine)
    yield engine
    SQLModel.metadata.drop_all(engine)

@pytest.fixture
def session(engine):
    SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
    db = SessionLocal()
    try:
        yield db
    finally:
        db.rollback()
        db.close()

from tests.fixtures.user_fixtures import USER
@pytest.fixture
def actor(session):
    user_dict = USER.dict()
    repo = UsersRepository(session)
    return repo.save(user_dict)
