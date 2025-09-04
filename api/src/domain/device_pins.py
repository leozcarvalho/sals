from typing import Optional
from sqlmodel import SQLModel, Field, Relationship
from src.domain.base import Base


class DevicePin(Base, table=True):
    __tablename__ = "device_pins"

    # Relação com o dispositivo
    instalation_id: int = Field(foreign_key="instalations.id", nullable=False)

    # Identificação do pino
    number: int = Field(nullable=False)  # ex: 1, 2, 3...
    name: Optional[str] = Field(default=None, max_length=50)  # apelido opcional

    # Estado do pino
    is_active: bool = Field(default=False, nullable=False)  # ligado/desligado
    mode: Optional[str] = Field(default=None, max_length=20)  # opcional
    svg_region_id: Optional[str] = Field(default=None, max_length=100)
    activation_color: Optional[str] = Field(default=None, max_length=20)  # ex: "#FF0000"

    # Relacionamento inverso
    device: Optional["Instalation"] = Relationship(back_populates="pins")
