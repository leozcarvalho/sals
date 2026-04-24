from sqlmodel import Field, Relationship
from typing import Optional
from src.domain.base import Base
from sqlalchemy import Numeric, Column
from decimal import Decimal

class ProductTank(Base, table=True):
    __tablename__ = "product_tanks"

    name: str = Field(nullable=False, max_length=100)
    description: Optional[str] = Field(default=None, max_length=255)
    product_id: int = Field(foreign_key="products.id", nullable=True)
    volume: Decimal = Field(sa_column=Column(Numeric(10, 2)), ge=0)
    is_dosador_seco: bool = Field(default=False)
    #Pino rosca
    screw_pin_id: int = Field(foreign_key="device_pins.id", nullable=True)
    #Pino balanca
    scale_pin_id: int = Field(foreign_key="device_pins.id", nullable=True)

    product: Optional["Product"] = Relationship(back_populates="tanks")
    kitchen_tanks: Optional[list["KitchenTank"]] = Relationship(
        back_populates="tank",
        sa_relationship_kwargs={"lazy": "selectin"}
    )

    screw_pin: Optional["DevicePin"] = Relationship(
        back_populates="screw_tanks",
        sa_relationship_kwargs={
            "foreign_keys": lambda: [ProductTank.screw_pin_id]
        }
    )

    scale_pin: Optional["DevicePin"] = Relationship(
        back_populates="scale_tanks",
        sa_relationship_kwargs={
            "foreign_keys": lambda: [ProductTank.scale_pin_id]
        }
    )