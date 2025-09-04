import pytest
from tests.fixtures.user_fixtures import user_repository, create_user, USER
from src.schemas import users as user_schemas
from src.resources import exceptions as exc

def test_user_creation(user_repository, actor):
    user_dict = USER.dict()
    user_dict['email'] = "teste@teste.com"
    user = user_repository.save(user_dict, actor=actor)
    assert user.id is not None
    assert user.name == "John"
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

def test_register_new_user_success(user_repository, actor):
    payload = user_schemas.UserCreatePayload(
        name="Alice",
        email="alice@example.com",
        password="secret123",
        confirm_password="secret123"
    )
    user = user_repository.register_new_user(payload)
    assert user.id is not None
    assert user.email == "alice@example.com"

def test_register_new_user_password_mismatch(user_repository):
    payload = user_schemas.UserCreatePayload(
        name="Bob",
        email="bob@example.com",
        password="123456",
        confirm_password="654321"
    )
    with pytest.raises(exc.InvalidData):
        user_repository.register_new_user(payload)

def test_request_password_reset_success(user_repository, create_user):
    user = create_user(email="reset@example.com")
    token = user_repository.request_password_reset("reset@example.com")
    assert token is not None
    db_user = user_repository.get(user.id)
    assert db_user.token_password == token

def test_request_password_reset_email_not_found(user_repository):
    with pytest.raises(exc.NotFound):
        user_repository.request_password_reset("notfound@example.com")

def test_reset_user_password_success(user_repository, create_user):
    user = create_user(email="reset2@example.com")
    token = user_repository.request_password_reset("reset2@example.com")
    
    reset_payload = user_schemas.UserResetPassword(
        token=token,
        new_password="newpass123",
        confirm_new_password="newpass123"
    )
    updated_user = user_repository.reset_user_password(reset_payload)
    assert updated_user is not None
    db_user = user_repository.get(user.id)
    assert db_user.token_password is None
    # Verifica se a senha foi atualizada (criptografada)
    assert db_user.encrypted_password != "newpass123"

def test_reset_user_password_invalid_token(user_repository):
    reset_payload = user_schemas.UserResetPassword(
        token="invalidtoken",
        new_password="123456",
        confirm_new_password="123456"
    )
    with pytest.raises(exc.NotFound):
        user_repository.reset_user_password(reset_payload)

def test_reset_user_password_mismatch(user_repository, create_user):
    user = create_user(email="mismatch@example.com")
    token = user_repository.request_password_reset("mismatch@example.com")
    reset_payload = user_schemas.UserResetPassword(
        token=token,
        new_password="abc123",
        confirm_new_password="xyz789"
    )
    with pytest.raises(exc.InvalidData):
        user_repository.reset_user_password(reset_payload)
