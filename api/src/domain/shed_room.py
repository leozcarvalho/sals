from typing import List, Optional
from sqlmodel import Field, Relationship
from src.domain.base import Base

class ShedRoom(Base, table=True):
    __tablename__ = "shed_rooms"

    name: str = Field(nullable=False, max_length=100)
    shed_id: int = Field(foreign_key="sheds.id", nullable=False)

    shed: Optional["Shed"] = Relationship(back_populates="rooms")
    stalls: List["RoomStall"] = Relationship(back_populates="room")
