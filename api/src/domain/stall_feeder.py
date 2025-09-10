from typing import Optional, List
from sqlmodel import Field, Relationship
from src.domain.base import Base

class StallFeeder(Base, table=True):
    __tablename__ = "stall_feeders"

    name: str = Field(nullable=False, max_length=100)
    room_stall_id: int = Field(foreign_key="room_stalls.id", nullable=False)

    room_stall: Optional["RoomStall"] = Relationship(back_populates="feeders")