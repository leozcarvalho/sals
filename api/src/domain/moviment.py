from typing import List, Optional
from sqlmodel import Field, Relationship
from src.domain.base import Base


class Moviment(Base, table=True):
    __tablename__ = "moviments"

    batch_id: int = Field(foreign_key="batches.id", nullable=False)
    moviment_kind_id: int = Field(foreign_key="moviment_kinds.id", nullable=False)
    stall_origin_id: Optional[int] = Field(foreign_key="room_stalls.id", nullable=True)
    stall_destination_id: Optional[int] = Field(foreign_key="room_stalls.id", nullable=True)
    quantity: int = Field(nullable=True)
    description: Optional[str] = Field(nullable=True)

    batch: "Batch" = Relationship(back_populates="moviments")
