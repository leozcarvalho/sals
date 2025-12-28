from typing import List, Optional
from sqlmodel import Field, Relationship
from src.domain.base import Base

class Shed(Base, table=True):
    __tablename__ = "sheds"

    name: str = Field(nullable=False, max_length=100)
    kitchen_id: int = Field(foreign_key="kitchens.id", nullable=False)

    salas: List["Sala"] = Relationship(back_populates="shed", sa_relationship_kwargs={"lazy": "selectin"})
    batch: "Batch" = Relationship(back_populates="shed")
    kitchen: "Kitchen" = Relationship(back_populates="sheds")
