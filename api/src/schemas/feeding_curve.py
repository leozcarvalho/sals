from pydantic.main import BaseModel
from typing import Optional, List
from src.schemas.global_schemas import BaseFilter, GlobalFields
from src.schemas.feeding_curve_detail import FeedingCurveDetail

class FeedingCurveBase(BaseModel):
    name: str
    description: Optional[str] = None
    is_active: bool = True
    details: Optional[List[FeedingCurveDetail]] = []

class FeedingCurveCreate(FeedingCurveBase):
    pass

class FeedingCurveUpdate(FeedingCurveBase):
    pass
class FeedingCurve(FeedingCurveBase, GlobalFields):
    pass

class FeedingCurveFilter(BaseFilter):
    pass
