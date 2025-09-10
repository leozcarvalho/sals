from pydantic.main import BaseModel
from typing import Optional, List
from src.schemas.global_schemas import BaseFilter, GlobalFields
from src.schemas.device_pins import DevicePin

class StallFeederBase(BaseModel):
    name: str
    room_stall_id: int

class StallFeederCreate(StallFeederBase):
    pass

class StallFeederUpdate(StallFeederBase):
    pass

class StallFeederPin(BaseModel):
    id: int
    pin: DevicePin

    class Config:
        from_attributes = True

class StallFeeder(StallFeederBase, GlobalFields):
    device_pins: Optional[List[StallFeederPin]] = []

class StallFeederFilter(BaseFilter):
    name: Optional[str] = None
    room_stall_id: Optional[int] = None
