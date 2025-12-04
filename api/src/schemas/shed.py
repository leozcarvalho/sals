from pydantic.main import BaseModel
from typing import Optional
from src.schemas.global_schemas import BaseFilter, GlobalFields
from src.schemas.shed_room import ShedRoom

class ShedBase(BaseModel):
    name: str

class ShedCreate(ShedBase):
    pass

class ShedUpdate(ShedBase):
    pass

class Shed(ShedBase, GlobalFields):
    rooms: Optional[list[ShedRoom]] = None

class ShedFilter(BaseFilter):
    name: Optional[str] = None
