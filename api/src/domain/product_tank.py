from sqlmodel import Field, Relationship
from typing import Optional
from src.domain.base import Base

class ProductTank(Base, table=True):
    __tablename__ = "product_tanks"

    name: str = Field(nullable=False, max_length=100)
    description: Optional[str] = Field(default=None, max_length=255)
    pin_id: int = Field(foreign_key="device_pins.id", nullable=False, unique=True)
    product_id: int = Field(foreign_key="products.id", nullable=False)

    device_pin: Optional["DevicePin"] = Relationship(back_populates="product_tanks")
    product: Optional["Product"] = Relationship(back_populates="tanks")
    kitchen_tanks: Optional[list["KitchenTank"]] = Relationship(
        back_populates="tank",
        sa_relationship_kwargs={"lazy": "selectin"}
    )