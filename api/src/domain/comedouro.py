from typing import Optional, List
from sqlmodel import Field, Relationship
from src.domain.base import Base
from src.domain.feeder_valves import FeederValve

class Comedouro(Base, table=True):
    __tablename__ = "comedouros"

    name: str = Field(nullable=False, max_length=100)
    baia_id: int = Field(foreign_key="baias.id", nullable=False)
    max_weight: float = Field(nullable=True)
    baia: Optional["Baia"] = Relationship(back_populates="comedouros")

