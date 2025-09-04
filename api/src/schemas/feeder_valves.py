from pydantic.main import BaseModel
from typing import Optional
from src.schemas.global_schemas import BaseFilter, GlobalFields

class FeederValveBase(BaseModel):
    device_pin_id: int
    stall_feeder_id: int

class FeederValveCreate(FeederValveBase):
    pass

class FeederValveUpdate(FeederValveBase):
    pass

class FeederValve(FeederValveBase, GlobalFields):
    pass

class FeederValveFilter(BaseFilter):
    device_pin_id: Optional[int] = None
    stall_feeder_id: Optional[int] = None
