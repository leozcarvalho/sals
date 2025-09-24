from sqlmodel import Field, Relationship
from src.domain.base import Base
from typing import Optional, List

class FormulaDetail(Base, table=True):
    __tablename__ = "formula_details"

    formula_id: int = Field(foreign_key="formulas.id", nullable=False)
    product_id: int = Field(foreign_key="products.id", nullable=False)
    product_percentage_without_moisture: int = Field(nullable=False, ge=0, le=100)

    formula: Optional["Formula"] = Relationship(back_populates="details")