import pytest
from tests.fixtures.user_fixture import user_service, create_user
from tests.fixtures.profile_fixture import create_profile

def test_get_user_by_id(user_service, create_user):
    user = create_user()
    user = user_service.get_by_id(user.id)
    assert user is not None
    assert user.id == user.id

def test_user_update(user_service, create_user):
    user = create_user()
    user.name = "Updated Name"
    user = user_service.update(user)
    assert user is not None
    assert user.name == "Updated Name"

def test_get_list_users(user_service, create_user):
    create_user(email="user1@test.com", name="User 1")
    create_user(email="user2@test.com", name="User 2")
    users = user_service.get_list()
    assert users is not None
    assert len(users) == 2
    assert users[0].email == "user1@test.com"
    assert users[1].email == "user2@test.com"