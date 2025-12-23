# conftest.py
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlmodel import SQLModel
from src import domain
from src.cruds.users import UsersRepository
from tests.fixtures.user_fixture import USER

@pytest.fixture(scope="session")
def engine():
    engine = create_engine(
        "sqlite:///:memory:",
        echo=False,
        future=True,
        connect_args={"check_same_thread": False},
    )
    SQLModel.metadata.create_all(engine)
    yield engine
    SQLModel.metadata.drop_all(engine)

@pytest.fixture
def session(engine):
    connection = engine.connect()
    transaction = connection.begin()

    SessionLocal = sessionmaker(
        bind=connection,
        autoflush=False,
        autocommit=False,
    )
    session = SessionLocal()

    try:
        yield session
    finally:
        session.close()
        transaction.rollback()
        connection.close()

@pytest.fixture
def actor(session):
    user_dict = USER.model_dump()
    user_dict['email'] = "test@admin.com"
    repo = UsersRepository(session)
    return repo.save(user_dict)
