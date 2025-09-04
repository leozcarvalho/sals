from pydantic.main import BaseModel
from typing import Optional
from src.schemas.global_schemas import BaseFilter, GlobalFields


class HardwarePointType(BaseModel):
    points_quantity: int
    kind: str

class HardwarePointTypeCreate(HardwarePointType):
    pass

class HardwarePointTypeUpdate(HardwarePointType):
    pass

class HardwarePointType(HardwarePointType, GlobalFields):
    pass

class HardwarePointTypeFilter(BaseFilter):
    points_quantity: Optional[int] = None
    kind: Optional[str] = None
