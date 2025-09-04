from pydantic.main import BaseModel
from typing import Optional
from src.schemas.global_schemas import BaseFilter, GlobalFields

class ShedRoomBase(BaseModel):
    name: str
    shed_id: int

class ShedRoomCreate(ShedRoomBase):
    pass

class ShedRoomUpdate(ShedRoomBase):
    pass

class ShedRoom(ShedRoomBase, GlobalFields):
    pass

class ShedRoomFilter(BaseFilter):
    name: Optional[str] = None
    shed_id: Optional[int] = None
