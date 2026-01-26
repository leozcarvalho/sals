from pydantic import BaseModel
from typing import List
from src.schemas.global_schemas import BaseFilter, GlobalFields
from decimal import Decimal

class TratoBase(BaseModel):
    name: str
    hour: int
    percent: Decimal

class TratoCreate(TratoBase):
    pass

class TratoUpdate(TratoBase):
    pass

class TratoRead(TratoBase, GlobalFields):
    pass

class TratoFilter(BaseFilter):
    pass

class TratoUpdateWithId(TratoUpdate):
    id: int

class BulkTratoUpdate(BaseModel):
    tratos: List[TratoUpdateWithId]