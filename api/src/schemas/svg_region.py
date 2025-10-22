from pydantic import BaseModel
from typing import Optional
from src.schemas.global_schemas import BaseFilter, GlobalFields

class SVGRegionBase(BaseModel):
    svg_id: int
    region_id: str
    pin_id: Optional[int] = None

class SVGRegionCreate(SVGRegionBase):
    pass

class SVGRegionUpdate(SVGRegionBase):
    pass

class SVGRegionRead(SVGRegionBase, GlobalFields):
    id: int
    owner_name: Optional[str] = None

class SVGRegionFilter(BaseFilter):
    pass
