from typing import List, Optional
from sqlmodel import Field, Relationship
from src.domain.base import Base

class Baia(Base, table=True):
    __tablename__ = "baias"

    name: str = Field(nullable=False, max_length=100)
    sala_id: int = Field(foreign_key="salas.id", nullable=False)
    animals_quantity: int = Field(default=0, nullable=False)

    sala: Optional["Sala"] = Relationship(back_populates="baias")
    comedouros: List["Comedouro"] = Relationship(back_populates="baia", sa_relationship_kwargs={"lazy": "selectin"})
