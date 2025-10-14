import pytest
from src.domain import exceptions as exc
from tests.fixtures.product_fixture import create_product, PRODUCT
from src.cruds.product import ProductRepository

@pytest.fixture
def product_repository(session) -> ProductRepository:
    return ProductRepository(session)

def test_create_product(product_repository):
    product = product_repository.save(PRODUCT.model_dump())
    assert product.id is not None
    assert product.name == "Água"

def test_update_product(session, product_repository):
    product = create_product(session)
    updated_product = product_repository.update(product.id, {"name": "Água Atualizada"})
    assert updated_product.name == "Água Atualizada"

def test_delete_product(session, product_repository):
    product = create_product(session, name="Produto Teste")
    deleted_product = product_repository.delete(product.id)
    assert deleted_product is not None
    assert product_repository.get(product.id) is None

def teste_agua_nao_pode_ser_deletada(session, product_repository):
    product = create_product(session, name="Água")
    with pytest.raises(exc.InvalidData) as exc_info:
        product_repository.delete(product.id)
    assert str(exc_info.value) == "Água não pode ser excluída"
