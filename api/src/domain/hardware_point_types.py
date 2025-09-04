from typing import List
from sqlmodel import Field, Relationship
from src.domain.base import Base


class PointType(Base, table=True):
    __tablename__ = "point_types"

    points_quantity: int = Field(nullable=False)
    kind: str = Field(nullable=False, max_length=255)
    devices: List["Device"] = Relationship(back_populates="point_type")