from typing import Optional
from decimal import Decimal
from sqlalchemy import Column, Numeric
from sqlmodel import Field, Relationship
from src.domain.base import Base


class Valve(Base, table=True):
    __tablename__ = "valves"

    name: str = Field(nullable=False, max_length=100)
    baia_id: int = Field(foreign_key="baias.id", nullable=False)
    device_pin_id: int = Field(foreign_key="device_pins.id", nullable=True)
    max_weight: Decimal = Field(sa_column=Column(Numeric(10, 2)))

    baia: "Baia" = Relationship(
        back_populates="valvulas",
        sa_relationship_kwargs={"lazy": "selectin"}
    )

    device_pin: Optional["DevicePin"] = Relationship(
        back_populates="valves",
        sa_relationship_kwargs={"lazy": "selectin"}
    )
