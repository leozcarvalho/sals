from sqlmodel import Field, Relationship
from typing import Optional
from src.domain.base import Base
from sqlalchemy import Column, Numeric
from decimal import Decimal


class DosadorSeco(Base, table=True):
    __tablename__ = "dosadores_secos"

    name: str = Field(nullable=False, max_length=100)

    #Pino de saida (para ligar uma rosca que tira dele, por exemplo)
    output_pin_id: int = Field(foreign_key="device_pins.id", nullable=True)

    #Balança
    scale_pin_id: int = Field(foreign_key="device_pins.id", nullable=True)

    #Peso máximo da cuba (kg)
    volume_misturador: Decimal = Field(sa_column=Column(Numeric(10, 2)))

    #Fração da cuba
    fracao_volume_misturador: Decimal = Field(sa_column=Column(Numeric(5, 2)))

    #Cozinha destino
    destiny_kitchen_id: int = Field(foreign_key="kitchens.id", nullable=True)

    #Ignorar peso na cozinha destino (toggle SIM NÃO)
    ignore_kitchen_weight: bool = Field(nullable=False, default=False)


    scale_pin: Optional["DevicePin"] = Relationship(
        sa_relationship_kwargs={"foreign_keys": "[DosadorSeco.scale_pin_id]"}
    )

    output_pin: Optional["DevicePin"] = Relationship(
        sa_relationship_kwargs={"foreign_keys": "[DosadorSeco.output_pin_id]"}
    )

    destiny_kitchen: Optional["Kitchen"] = Relationship(
        sa_relationship_kwargs={"foreign_keys": "[DosadorSeco.destiny_kitchen_id]"}
    )
