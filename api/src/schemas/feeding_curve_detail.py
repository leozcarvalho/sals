from pydantic.main import BaseModel
from src.schemas.global_schemas import BaseFilter, GlobalFields

class FeedingCurveDetailBase(BaseModel):
    curve_id: int
    age_day: int
    formula_id: int
    formula_mass: float
    is_active: bool = True

class FeedingCurveDetCreate(FeedingCurveDetailBase):
    pass

class FeedingCurveDetUpdate(FeedingCurveDetailBase):
    pass

class FeedingCurveDetRead(FeedingCurveDetailBase, GlobalFields):
    pass

class FeedingCurveDetFilter(BaseFilter):
    pass
