import pytest
from src.cruds.feeding_curve_detail import FeedingCurveDetRepository
from src.schemas.feeding_curve_detail import FeedingCurveDetCreate

FEEDING_CURVE_DETAIL = FeedingCurveDetCreate(
    curve_id=1,
    age_day=22,
    formula_id=1,
    formula_mass=2.500,
    is_active=True
)

def create_feeding_curve_detail(session, actor=None, **overrides):
    repo = FeedingCurveDetRepository(session)
    data = FEEDING_CURVE_DETAIL.model_dump()
    data.update(overrides)
    feeding_curve_detail = repo.save(data, actor=actor)
    return feeding_curve_detail
