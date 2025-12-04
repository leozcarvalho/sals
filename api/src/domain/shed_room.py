from typing import List, Optional
from sqlmodel import Field, Relationship
from src.domain.base import Base

class ShedRoom(Base, table=True):
    __tablename__ = "shed_rooms"

    name: str = Field(nullable=False, max_length=100)
    shed_id: int = Field(foreign_key="sheds.id", nullable=False)
    entrance_pin_id: int = Field(foreign_key="device_pins.id", nullable=True)

    shed: "Shed" = Relationship(back_populates="rooms")
    stalls: List["RoomStall"] = Relationship(back_populates="room")
    entrance_pin: Optional["DevicePin"] = Relationship()
    batch: "Batch" = Relationship(back_populates="shed_room")
