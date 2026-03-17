import pytest
from src.domain import exceptions as exc
from tests.fixtures.formula_fixture import create_formula, FORMULA
from tests.fixtures.product_fixture import create_product
from src.cruds.formula import FormulaRepository

@pytest.fixture
def formula_repository(session) -> FormulaRepository:
    return FormulaRepository(session)

@pytest.fixture
def get_detail_data(session):
    product_1 = create_product(session, name="Água")
    product_2 = create_product(session, name="Óleo")
    details = [
        {"product_id": product_1.id, "product_percentage_without_moisture": 70},
        {"product_id": product_2.id, "product_percentage_without_moisture": 30}
    ]
    return lambda: details

def test_create_formula(formula_repository, get_detail_data):
    details = get_detail_data()
    data = FORMULA.model_dump().copy()
    data["details"] = details
    formula = formula_repository.save(data)
    assert formula.id is not None
    assert formula.name == "Fórmula Padrão"

def test_update_formula(session, formula_repository, get_detail_data):
    details = get_detail_data()
    formula = create_formula(session, details=details)
    updated_formula = formula_repository.update(formula.id, {"name": "Fórmula Atualizada"})
    assert updated_formula.name == "Fórmula Atualizada"

def test_invalid_details_sum(session, formula_repository, get_detail_data):
    details = get_detail_data()
    details[0]['product_percentage_without_moisture'] = 80  # Invalid sum (80 + 30 != 100)
    data = FORMULA.model_dump().copy()
    data["details"] = details
    with pytest.raises(exc.InvalidData) as exc_info:
        formula_repository.save(data)
    assert str(exc_info.value) == "A soma das porcentagens dos produtos deve ser igual a 100%."
