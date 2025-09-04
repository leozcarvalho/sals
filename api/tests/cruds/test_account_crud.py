import pytest
from tests.fixtures.account_fixture import create_account, account_repository
from src.schemas.accounts import Account
from src.resources import exceptions as exc

def test_create_account(create_account):
    account = create_account(name="Conta Criada")
    assert account.id is not None
    assert account.name == "Conta Criada"
    assert account.is_active is True

def test_update_account(create_account, account_repository, actor):
    account = create_account(name="Conta Inicial")
    update_data = {"name": "Conta Atualizada", "is_active": False}
    updated_account = account_repository.update(account.id, update_data, actor=actor)
    
    assert updated_account.name == "Conta Atualizada"
    assert updated_account.is_active is False

def test_delete_account(create_account, account_repository):
    account = create_account(name="Conta para Deletar")
    account_repository.delete(account.id)
    
    deleted_account = account_repository.get(account.id)
    assert deleted_account is None

def test_get_list_accounts(create_account, account_repository):
    # cria algumas contas
    create_account(name="Conta 1")
    create_account(name="Conta 2", is_active=False)
    
    accounts = account_repository.get_list()
    names = [a.name for a in accounts]
    
    assert "Conta 1" in names
    assert "Conta 2" in names
    # pelo menos duas contas devem existir
    assert len(accounts) >= 2

def test_update_account_not_found(account_repository, actor):
    with pytest.raises(exc.NotFound):
        account_repository.update(9999, {"name": "Não Existe"}, actor=actor)

def test_delete_account_not_found(account_repository):
    with pytest.raises(exc.NotFound):
        account_repository.delete(9999)