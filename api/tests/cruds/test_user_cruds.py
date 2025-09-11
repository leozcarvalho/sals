import pytest
from tests.fixtures.user_fixture import user_repository, create_user, USER
from src.schemas import users as user_schemas
from src.domain import exceptions as exc

def test_user_creation(user_repository, actor):
    user_dict = USER.model_dump()
    user_dict['email'] = "teste@teste.com"
    user = user_repository.save(user_dict, actor=actor)
    assert user.id is not None
    assert user.email == "teste@teste.com"

def test_update_user(user_repository, create_user, actor):
    user = create_user(name="Jane", email="jane@example.com")
    update_data = {
        "name": "Jane Doe",
        "email": "jane.doe@updated.com"
    }
    user = user_repository.update(user.id, update_data, actor=actor)
    assert user.name == "Jane Doe"
    assert user.email == "jane.doe@updated.com"
