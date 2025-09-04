from pydantic.main import BaseModel
from typing import Optional
from src.schemas.global_schemas import BaseFilter, GlobalFields

class RoomStallBase(BaseModel):
    name: str
    shed_room_id: int

class RoomStallCreate(RoomStallBase):
    pass

class RoomStallUpdate(RoomStallBase):
    pass

class RoomStall(RoomStallBase, GlobalFields):
    pass

class RoomStallFilter(BaseFilter):
    name: Optional[str] = None
    shed_room_id: Optional[int] = None
