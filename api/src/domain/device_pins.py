from typing import Optional, List
from sqlmodel import SQLModel, Field, Relationship
from src.domain.base import Base


class DevicePin(Base, table=True):
    __tablename__ = "device_pins"

    # Relação com o dispositivo
    installation_id: int = Field(foreign_key="installations.id", nullable=False)

    # Identificação do pino
    number: int = Field(nullable=False)  # ex: 1, 2, 3...
    name: Optional[str] = Field(default=None, max_length=50)  # apelido opcional

    # Estado do pino
    is_active: bool = Field(default=False, nullable=False)  # ligado/desligado
    mode: Optional[str] = Field(default=None, max_length=20)  # opcional
    svg_region_id: Optional[str] = Field(default=None, max_length=100)
    activation_color: Optional[str] = Field(default=None, max_length=20)  # ex: "#FF0000"

    installation: Optional["Installation"] = Relationship(
        back_populates="pins",
        sa_relationship_kwargs={"lazy": "selectin"}  # evita cartesian product
    )

    # Relação com tanques de produto
    product_tanks: Optional[List["ProductTank"]] = Relationship(
        back_populates="device_pin",
        sa_relationship_kwargs={"lazy": "selectin"}
    )
