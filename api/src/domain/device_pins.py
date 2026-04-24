from typing import Optional, List
from sqlmodel import SQLModel, Field, Relationship
from src.domain.base import Base
from src.domain.valves import Valve

class DevicePin(Base, table=True):
    __tablename__ = "device_pins"

    # Relação com o dispositivo
    installation_id: int = Field(foreign_key="installations.id", nullable=False)

    # Identificação do pino
    number: int = Field(nullable=False)  # ex: 1, 2, 3...
    name: str = Field(nullable=False, max_length=50)

    # Estado do pino
    is_active: bool = Field(default=False, nullable=False)  # ligado/desligado

    installation: Optional["Installation"] = Relationship(
        back_populates="pins",
        sa_relationship_kwargs={"lazy": "selectin"}
    )

    screw_tanks: Optional[List["ProductTank"]] = Relationship(
        back_populates="screw_pin",
        sa_relationship_kwargs={
            "foreign_keys": "[ProductTank.screw_pin_id]"
        }
    )

    scale_tanks: Optional[List["ProductTank"]] = Relationship(
        back_populates="scale_pin",
        sa_relationship_kwargs={
            "foreign_keys": "[ProductTank.scale_pin_id]"
        }
    )

    valves: Optional[List["Valve"]] = Relationship(
        back_populates="device_pin",
        sa_relationship_kwargs={"lazy": "selectin"}
    )

    @property
    def arbitrary_name(self) -> str:
        return f"D{self.installation_id}P{self.number}"
