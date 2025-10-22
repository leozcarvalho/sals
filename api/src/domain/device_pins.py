from typing import Optional, List
from sqlmodel import SQLModel, Field, Relationship
from src.domain.base import Base


class DevicePin(Base, table=True):
    __tablename__ = "device_pins"

    # Relação com o dispositivo
    installation_id: int = Field(foreign_key="installations.id", nullable=False)

    # Identificação do pino
    number: int = Field(nullable=False)  # ex: 1, 2, 3...
    name: str = Field(nullable=False, max_length=50)

    # Estado do pino
    is_active: bool = Field(default=False, nullable=False)  # ligado/desligado
    mode: Optional[str] = Field(default=None, max_length=20)  # opcional

    installation: Optional["Installation"] = Relationship(
        back_populates="pins",
        sa_relationship_kwargs={"lazy": "selectin"}
    )

    product_tanks: Optional[List["ProductTank"]] = Relationship(
        back_populates="device_pin",
        sa_relationship_kwargs={"lazy": "selectin"}
    )

    feeder_valves: Optional[List["FeederValve"]] = Relationship(
        back_populates="device_pin",
        sa_relationship_kwargs={"lazy": "selectin"}
    )