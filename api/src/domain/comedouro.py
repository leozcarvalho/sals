from typing import Optional
from sqlmodel import Field, Relationship
from src.domain.base import Base
from sqlalchemy import Column, Numeric
from decimal import Decimal

class Comedouro(Base, table=True):
    __tablename__ = "comedouros"

    name: str = Field(nullable=False, max_length=100)
    baia_id: int = Field(foreign_key="baias.id", nullable=False)
    max_weight: Decimal = Field(sa_column=Column(Numeric(10, 2)))
    baia: Optional["Baia"] = Relationship(back_populates="comedouros")
