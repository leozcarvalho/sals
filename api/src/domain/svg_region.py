from typing import List, Optional
from sqlmodel import Field, Relationship
from src.domain.base import Base

class SVGRegion(Base, table=True):
    __tablename__ = "svg_regions"

    svg_id: int = Field(foreign_key="svgs.id", nullable=False)
    region_id: str = Field(nullable=False, max_length=100)
    pin_id: Optional[int] = Field(foreign_key="device_pins.id", default=None)
