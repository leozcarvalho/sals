from sqlmodel import Field, Relationship
from typing import Optional
from src.domain.base import Base

class Product(Base, table=True):
    __tablename__ = "products"

    name: str = Field(nullable=False, max_length=100)
    description: str = Field(nullable=True, max_length=255)
    moisture_percentage: int = Field(nullable=False, ge=0, le=100) # porcentagem de umidade
    kind: str = Field(nullable=False, max_length=10)  # 'solid' or 'liquid'
    density: int = Field(nullable=False, ge=0, le=10000)
    is_active: bool = Field(nullable=False, default=True)

    tanks: Optional[list["ProductTank"]] = Relationship(
        back_populates="product",
        sa_relationship_kwargs={"lazy": "selectin"}
    )
