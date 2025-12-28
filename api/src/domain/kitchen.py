from typing import Optional, List
from sqlmodel import Field, Relationship
from src.domain.base import Base
from sqlalchemy import Column, Numeric
from decimal import Decimal

class Kitchen(Base, table=True):
    __tablename__ = "kitchens"

    name: str = Field(nullable=False, max_length=100)

    # Pinos
    shaker_pin_id: int = Field(foreign_key="device_pins.id", nullable=False)
    pump_pin_id: int = Field(foreign_key="device_pins.id", nullable=False)
    scale_pin_id: int = Field(foreign_key="device_pins.id", nullable=False)

    max_bowl_weight: Decimal = Field(sa_column=Column(Numeric(10, 2)))
    bowl_weight_fraction: Decimal = Field(sa_column=Column(Numeric(5, 2)))

    shaker_pin: Optional["DevicePin"] = Relationship(
        sa_relationship_kwargs={"foreign_keys": "[Kitchen.shaker_pin_id]"}
    )
    pump_pin: Optional["DevicePin"] = Relationship(
        sa_relationship_kwargs={"foreign_keys": "[Kitchen.pump_pin_id]"}
    )
    scale_pin: Optional["DevicePin"] = Relationship(
        sa_relationship_kwargs={"foreign_keys": "[Kitchen.scale_pin_id]"}
    )
    tanks: List["KitchenTank"] = Relationship(
        back_populates="kitchen",
        sa_relationship_kwargs={"cascade": "all, delete-orphan"}
    )
    sheds: List["Shed"] = Relationship(back_populates="kitchen")