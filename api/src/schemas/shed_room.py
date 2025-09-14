from pydantic.main import BaseModel
from typing import Optional
from src.schemas.global_schemas import BaseFilter, GlobalFields
from src.schemas.device_pins import DevicePin

class ShedRoomBase(BaseModel):
    name: str
    shed_id: int
    entrance_pin_id: Optional[int] = None

class ShedRoomCreate(ShedRoomBase):
    pass

class ShedRoomUpdate(ShedRoomBase):
    pass

class ShedRoom(ShedRoomBase, GlobalFields):
    entrance_pin: Optional[DevicePin] = None


class ShedRoomFilter(BaseFilter):
    name: Optional[str] = None
    shed_id: Optional[int] = None
