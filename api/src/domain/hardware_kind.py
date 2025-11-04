from typing import List
from sqlmodel import Field, Relationship
from src.domain.base import Base
from enum import Enum

class HardwareKindEnum(str, Enum):
    OUTPUT = "output"
    INPUT = "input"

class HardwareKind(Base, table=True):
    __tablename__ = "hardware_kinds"

    name: str = Field(nullable=False, max_length=255)
    kind: HardwareKindEnum = Field(nullable=False)
    devices: List["Device"] = Relationship(back_populates="hardware_kind")
