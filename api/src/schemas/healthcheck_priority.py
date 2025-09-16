from pydantic.main import BaseModel
from typing import Optional
from src.schemas.global_schemas import BaseFilter, GlobalFields

class HealthcheckPriorityBase(BaseModel):
    name: str
    level: int
    interval_seconds: int


class HealthcheckPriorityCreate(HealthcheckPriorityBase):
    pass

class HealthcheckPriorityUpdate(HealthcheckPriorityBase):
    pass

class HealthcheckPriority(HealthcheckPriorityBase, GlobalFields):
    pass

class HealthcheckPriorityFilter(BaseFilter):
    name: Optional[str] = None
    level: Optional[int] = None
    interval_seconds: Optional[int] = None
