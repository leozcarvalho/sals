from sqlmodel import Field, Relationship
from typing import Optional
from src.domain.base import Base

class KitchenProduct(Base, table=True):
    __tablename__ = "kitchen_products"

    device_pin_id: int = Field(foreign_key="device_pins.id", nullable=False, unique=True)
    kitchen_id: int = Field(foreign_key="kitchens.id", nullable=False)

    device_pin: Optional["DevicePin"] = Relationship(back_populates="kitchen_products")
    kitchen: Optional["Kitchen"] = Relationship(back_populates="products")