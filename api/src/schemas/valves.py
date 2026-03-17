from pydantic.main import BaseModel
from typing import Optional
from decimal import Decimal
from src.schemas.global_schemas import BaseFilter, GlobalFields
from src.schemas.device_pins import DevicePin

class ValveBase(BaseModel):
    name: str 
    device_pin_id: Optional[int] = None
    baia_id: int
    max_weight: Decimal

class ValveCreate(ValveBase):
    pass

class ValveUpdate(ValveBase):
    pass

class Valve(ValveBase, GlobalFields):
    device_pin: Optional[DevicePin] = None

class ValveFilter(BaseFilter):
    device_pin_id: Optional[int] = None
    baia_id: Optional[int] = None
