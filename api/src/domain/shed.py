from typing import List
from sqlmodel import Field, Relationship
from src.domain.base import Base

class Shed(Base, table=True):
    __tablename__ = "sheds"

    name: str = Field(nullable=False, max_length=100)
    entrance_pin_id: int = Field(foreign_key="device_pins.id", nullable=True)

    rooms: List["ShedRoom"] = Relationship(back_populates="shed")
