from pydantic import BaseModel
from typing import Optional, List
from src.schemas.global_schemas import BaseFilter, GlobalFields

class SVGBase(BaseModel):
    name: str
    owner_type: str
    owner_id: int
    content: str

class SVGCreate(SVGBase):
    pass

class SVGUpdate(SVGBase):
    pass

class SVGRead(SVGBase, GlobalFields):
    id: int
    owner_name: Optional[str] = None

class SVGFilter(BaseFilter):
    name: Optional[str] = None
    owner_type: Optional[str] = None
    owner_id: Optional[int] = None
