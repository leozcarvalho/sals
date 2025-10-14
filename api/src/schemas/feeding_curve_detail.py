from pydantic.main import BaseModel
from decimal import Decimal
from src.schemas.global_schemas import BaseFilter, GlobalFields

class FeedingCurveDetailBase(BaseModel):
    age_day: int
    formula_id: int
    formula_mass_per_animal: Decimal
    animal_weight: Decimal
    is_active: bool = True

class FeedingCurveDetailCreate(FeedingCurveDetailBase):
    feeding_curve_id: int

class FeedingCurveDetailUpdate(FeedingCurveDetailBase):
    feeding_curve_id: int

class FeedingCurveDetailRead(FeedingCurveDetailBase, GlobalFields):
    pass

class FeedingCurveDetailFilter(BaseFilter):
    pass
