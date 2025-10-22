from src.cruds.feeding_curve import FeedingCurveRepository
from src.schemas.feeding_curve import FeedingCurveCreate

FEEDING_CURVE = FeedingCurveCreate(
    name="Curva Inicial",
    description="Curva padrão",
    is_active=True
)

def create_feeding_curve(session, actor=None, **overrides):
    repo = FeedingCurveRepository(session)
    data = FEEDING_CURVE.model_dump()
    data.update(overrides)
    feeding_curve = repo.save(data, actor=actor)
    return feeding_curve