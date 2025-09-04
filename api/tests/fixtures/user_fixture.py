import pytest
from src.cruds.users import UsersRepository
from src.schemas.users import UserCreate

@pytest.fixture
def user_repository(session) -> UsersRepository:
    return UsersRepository(session)

USER = UserCreate(
    name="Test User",
    email="test@example.com",
    password="123456",
    is_active=True,
    profile_id=1
)

@pytest.fixture()
def create_user(user_repository: UsersRepository, actor):
    def _create_user(**overrides):
        user_dict = USER.model_dump()
        user_dict.update(overrides)
        user = UserCreate(**user_dict)
        user = user_repository.save(user.model_dump(), actor=actor)
        return user
    return _create_user
