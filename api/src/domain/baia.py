from typing import List, Optional
from sqlmodel import Field, Relationship
from src.domain.base import Base
from sqlalchemy import Column, Numeric
from decimal import Decimal

class Baia(Base, table=True):
    __tablename__ = "baias"

    name: str = Field(nullable=False, max_length=100)
    sala_id: int = Field(foreign_key="salas.id", nullable=False)
    animals_quantity: int = Field(default=0, nullable=False)
    t1: Decimal = Field(sa_column=Column(Numeric(10, 2)), default=0)
    t2: Decimal = Field(sa_column=Column(Numeric(10, 2)), default=0)
    t3: Decimal = Field(sa_column=Column(Numeric(10, 2)), default=0)
    t4: Decimal = Field(sa_column=Column(Numeric(10, 2)), default=0)
    t5: Decimal = Field(sa_column=Column(Numeric(10, 2)), default=0)
    t6: Decimal = Field(sa_column=Column(Numeric(10, 2)), default=0)

    sala: Optional["Sala"] = Relationship(back_populates="baias")
    comedouros: List["Comedouro"] = Relationship(back_populates="baia", sa_relationship_kwargs={"lazy": "selectin"})
