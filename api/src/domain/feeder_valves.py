from typing import Optional
from sqlmodel import Field
from src.domain.base import Base


class FeederValve(Base, table=True):
    __tablename__ = "feeder_valves"

    stall_feeder_id: int = Field(foreign_key="stall_feeders.id", nullable=False)
    device_pin_id: int = Field(foreign_key="device_pins.id", nullable=False)