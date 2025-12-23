from typing import Optional
from sqlmodel import Field, Relationship
from src.domain.base import Base


class FeederValve(Base, table=True):
    __tablename__ = "feeder_valves"

    comedouro_id: int = Field(foreign_key="comedouros.id", nullable=False)
    device_pin_id: int = Field(foreign_key="device_pins.id", nullable=False)

    device_pin: Optional["DevicePin"] = Relationship(
        back_populates="feeder_valves",
        sa_relationship_kwargs={"lazy": "selectin"}
    )
