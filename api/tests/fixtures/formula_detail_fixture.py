import pytest
from src.cruds.formula_detail import FormulaDetailRepository
from src.schemas.formula_detail import FormulaDetailCreate

FORMULA_DETAIL = FormulaDetailCreate(
    formula_id=1,
    product_id=1,
    product_percentage_without_moisture=100
)

def create_formula_detail(session, actor=None, **overrides):
    repo = FormulaDetailRepository(session)
    data = FORMULA_DETAIL.model_dump()
    data.update(overrides)
    formula_detail = repo.save(data, actor=actor)
    return formula_detail
