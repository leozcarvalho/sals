from pydantic.main import BaseModel
from typing import Optional
from src.schemas.global_schemas import BaseFilter, GlobalFields

class FeedingCurveBase(BaseModel):
    name: str
    description: Optional[str] = None
    is_active: bool = True

class FeedingCurveCreate(FeedingCurveBase):
    pass

class FeedingCurveUpdate(FeedingCurveBase):
    pass

class FeedingCurveRead(FeedingCurveBase, GlobalFields):
    pass

class FeedingCurveFilter(BaseFilter):
    pass
