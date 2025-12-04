from typing import List, Optional
from sqlmodel import Field, Relationship
from src.domain.base import Base

class RoomStall(Base, table=True):
    __tablename__ = "room_stalls"

    name: str = Field(nullable=False, max_length=100)
    shed_room_id: int = Field(foreign_key="shed_rooms.id", nullable=False)
    animals_quantity: int = Field(default=0, nullable=False)

    room: Optional["ShedRoom"] = Relationship(back_populates="stalls")
    feeders: List["StallFeeder"] = Relationship(back_populates="room_stall")
