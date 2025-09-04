from typing import List
from sqlmodel import Field, Relationship
from src.domain.base import Base

class HardwareKind(Base, table=True):
    __tablename__ = "hardware_kinds"

    kind: str = Field(nullable=False, max_length=255)
    devices: List["Device"] = Relationship(back_populates="hardware_kind")