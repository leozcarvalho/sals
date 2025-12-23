from pydantic.main import BaseModel
from typing import Optional, List
from src.schemas.global_schemas import BaseFilter, GlobalFields
from src.schemas.sala import Sala

class ShedBase(BaseModel):
    name: str

class ShedCreate(ShedBase):
    pass

class ShedUpdate(ShedBase):
    pass

class Shed(ShedBase, GlobalFields):
    salas: Optional[List[Sala]] = None

class ShedFilter(BaseFilter):
    name: Optional[str] = None
