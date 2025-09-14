import pytest
from src.cruds.users import UsersRepository
from src.schemas.users import UserCreate

USER = UserCreate(
    name="Test User",
    email="test@example.com",
    password="123456",
    is_active=True,
    profile_id=1
)

def create_user(session, actor=None, **overrides):
    repo = UsersRepository(session)
    user_dict = USER.model_dump()
    user_dict.update(overrides)
    user = UserCreate(**user_dict)
    user = repo.save(user.model_dump(), actor=actor)
    return user
