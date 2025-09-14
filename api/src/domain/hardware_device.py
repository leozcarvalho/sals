from typing import List, Optional
from sqlmodel import Field, Relationship
from src.domain.base import Base

class Device(Base, table=True):
    __tablename__ = "devices"

    name: str = Field(nullable=False, max_length=255)
    connection_template_id: int = Field(foreign_key="connection_templates.id", nullable=False)
    hardware_kind_id: int = Field(foreign_key="hardware_kinds.id", nullable=False)
    point_type_id: int = Field(foreign_key="point_types.id", nullable=False)
    svg_template: Optional[str] = Field(default=None)

    connection_template: Optional["ConnectionTemplate"] = Relationship(back_populates="devices")
    hardware_kind: Optional["HardwareKind"] = Relationship(back_populates="devices")
    point_type: Optional["PointType"] = Relationship(back_populates="devices")
    installations: List["Installation"] = Relationship(
        back_populates="device",
        sa_relationship_kwargs={"lazy": "selectin"}
    )