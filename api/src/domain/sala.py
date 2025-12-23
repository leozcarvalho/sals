from typing import List, Optional
from sqlmodel import Field, Relationship
from src.domain.base import Base

class Sala(Base, table=True):
    __tablename__ = "salas"

    name: str = Field(nullable=False, max_length=100)
    shed_id: int = Field(foreign_key="sheds.id", nullable=False)
    entrance_pin_id: int = Field(foreign_key="device_pins.id", nullable=True)

    shed: "Shed" = Relationship(back_populates="salas")
    baias: List["Baia"] = Relationship(back_populates="sala", sa_relationship_kwargs={"lazy": "selectin"})
    entrance_pin: Optional["DevicePin"] = Relationship()
    batch: "Batch" = Relationship(back_populates="sala")
