from pydantic.main import BaseModel
from typing import Optional
from src.schemas.global_schemas import BaseFilter, GlobalFields

class ShedBase(BaseModel):
    name: str

class ShedCreate(ShedBase):
    pass

class ShedUpdate(ShedBase):
    pass

class Shed(ShedBase, GlobalFields):
    pass

class ShedFilter(BaseFilter):
    name: Optional[str] = None
