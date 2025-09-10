from pydantic.main import BaseModel
from typing import Optional
from src.schemas.global_schemas import BaseFilter, GlobalFields
from src.schemas.device_pins import DevicePin

class ShedBase(BaseModel):
    name: str
    entrance_pin_id: Optional[int] = None

class ShedCreate(ShedBase):
    pass

class ShedUpdate(ShedBase):
    pass

class Shed(ShedBase, GlobalFields):
    entrance_pin: Optional[DevicePin] = None

class ShedFilter(BaseFilter):
    name: Optional[str] = None
