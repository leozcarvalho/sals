from sqlmodel import Field, Relationship
from src.domain.base import Base
from typing import Optional, List

class Batch(Base, table=True):
    __tablename__ = "batches"

    name: str = Field(nullable=False, max_length=100)
    description: str = Field(nullable=True, max_length=255)
    
    #Deve vir dos dias cadastrados na curva de alimentação
    initial_day: int = Field(nullable=False)

    is_active: bool = Field(nullable=False, default=True)
    feeding_curve_id: int = Field(foreign_key="feeding_curves.id", nullable=False)
    shed_id: int = Field(foreign_key="sheds.id", nullable=False)
    sala_id: int = Field(foreign_key="salas.id", nullable=False)

    shed: "Shed" = Relationship(back_populates="batch")
    sala: "Sala" = Relationship(back_populates="batch")
    feeding_curve: "FeedingCurve" = Relationship(back_populates="batch")

    moviments: List["Moviment"] = Relationship(back_populates="batch")
