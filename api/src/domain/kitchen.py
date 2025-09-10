from typing import Optional
from sqlmodel import Field, Relationship
from src.domain.base import Base

class Kitchen(Base, table=True):
    __tablename__ = "kitchens"

    name: str = Field(nullable=False, max_length=100)

    # Pinos
    shaker_pin_id: int = Field(foreign_key="device_pins.id", nullable=False)
    pump_pin_id: int = Field(foreign_key="device_pins.id", nullable=False)
    scale_pin_id: int = Field(foreign_key="device_pins.id", nullable=False)
    #TODO: PRODUTO é 1 pra N

    shaker_pin: Optional["DevicePin"] = Relationship(sa_relationship_kwargs={"foreign_keys": "[Kitchen.shaker_pin_id]"})
    pump_pin: Optional["DevicePin"] = Relationship(sa_relationship_kwargs={"foreign_keys": "[Kitchen.pump_pin_id]"})
    scale_pin: Optional["DevicePin"] = Relationship(sa_relationship_kwargs={"foreign_keys": "[Kitchen.scale_pin_id]"})
