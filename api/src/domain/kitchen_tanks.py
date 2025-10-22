from sqlmodel import Field, Relationship
from typing import Optional
from src.domain.base import Base

class KitchenTank(Base, table=True):
    __tablename__ = "kitchen_tanks"

    product_tank_id: int = Field(foreign_key="product_tanks.id", nullable=False)
    kitchen_id: int = Field(foreign_key="kitchens.id", nullable=False)

    kitchen: Optional["Kitchen"] = Relationship(back_populates="tanks")
    tank: Optional["ProductTank"] = Relationship(back_populates="kitchen_tanks")
