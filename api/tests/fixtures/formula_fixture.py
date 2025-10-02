import pytest
from src.cruds.formula import FormulaRepository
from src.schemas.formula import FormulaCreate

FORMULA = FormulaCreate(
    name="Fórmula Padrão",
    description="Fórmula inicial",
    water_percentage=50,
    stirring_time=600,
    is_active=True
)

def create_formula(session, actor=None, **overrides):
    repo = FormulaRepository(session)
    data = FORMULA.model_dump()
    data.update(overrides)
    formula = repo.save(data, actor=actor)
    return formula