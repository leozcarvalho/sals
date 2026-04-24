from sqlmodel import Field, Relationship
from src.domain.base import Base
from typing import Optional, List
from decimal import Decimal
from sqlalchemy import Numeric, Column

class FormulaDetail(Base, table=True):
    __tablename__ = "formula_details"

    formula_id: int = Field(foreign_key="formulas.id", nullable=False)
    product_id: int = Field(foreign_key="products.id", nullable=False)
    product_percentage_without_moisture: Decimal = Field(sa_column=Column(Numeric(10, 3)), ge=0)

    formula: Optional["Formula"] = Relationship(back_populates="details")
    product: Optional["Product"] = Relationship(back_populates="formula_details")