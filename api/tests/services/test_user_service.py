import pytest
from tests.fixtures.user_fixture import user_repository, create_user
from tests.fixtures.profile_fixture import create_profile

def test_get_user_by_id(user_repository, create_user):
    user = create_user()
    user = user_repository.get(user.id)
    assert user is not None
    assert user.id == user.id

def test_user_update(user_repository, create_user):
    user = create_user()
    user.name = "Updated Name"
    user = user_repository.update(user.id, user.model_dump())
    assert user is not None
    assert user.name == "Updated Name"

def test_get_list_users(user_repository, create_user):
    create_user(email="user1@test.com", name="User 1")
    create_user(email="user2@test.com", name="User 2")
    users = user_repository.get_list()
    assert users is not None
    assert len(users) == 3
