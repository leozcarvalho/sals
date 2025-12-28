from pydantic.main import BaseModel
from typing import Optional, List
from src.schemas.global_schemas import BaseFilter, GlobalFields
from src.schemas.sala import Sala
from src.schemas.kicthen import Kitchen

class ShedBase(BaseModel):
    name: str
    kitchen_id: int

class ShedCreate(ShedBase):
    pass

class ShedUpdate(ShedBase):
    pass

class Shed(ShedBase, GlobalFields):
    salas: Optional[List[Sala]] = None
    kitchen: Kitchen

class ShedFilter(BaseFilter):
    name: Optional[str] = None
