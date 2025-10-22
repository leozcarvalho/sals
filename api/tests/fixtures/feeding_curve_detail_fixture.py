from src.cruds.feeding_curve_detail import FeedingCurveDetailRepository
from src.schemas.feeding_curve_detail import FeedingCurveDetailCreate

FEEDING_CURVE_DETAIL = FeedingCurveDetailCreate(
    feeding_curve_id=1,
    age_day=22,
    formula_id=1,
    formula_mass_per_animal=2.500,
    animal_weight=150.0,
    is_active=True
)

def create_feeding_curve_detail(session, actor=None, **overrides):
    repo = FeedingCurveDetailRepository(session)
    data = FEEDING_CURVE_DETAIL.model_dump()
    data.update(overrides)
    feeding_curve_detail = repo.save(data, actor=actor)
    return feeding_curve_detail
