from pydantic.main import BaseModel
from typing import Optional
from src.schemas.global_schemas import BaseFilter, GlobalFields
from src.schemas.device_pins import DevicePin

class FeederValveBase(BaseModel):
    device_pin_id: int
    comedouro_id: int

class FeederValveCreate(FeederValveBase):
    pass

class FeederValveUpdate(FeederValveBase):
    pass

class FeederValve(FeederValveBase, GlobalFields):
    device_pin: Optional[DevicePin] = None

class FeederValveFilter(BaseFilter):
    device_pin_id: Optional[int] = None
    comedouro_id: Optional[int] = None
