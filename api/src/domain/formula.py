from sqlmodel import Field, Relationship
from src.domain.base import Base
from typing import Optional, List

class Formula(Base, table=True):
    __tablename__ = "formulas"

    name: str = Field(nullable=False, max_length=100)
    description: str = Field(nullable=True, max_length=255)
    water_percentage: int = Field(nullable=False, ge=0, le=100)
    stirring_time: int = Field(nullable=False, ge=0, le=7200)
    is_active: bool = Field(nullable=False, default=True)

    details: Optional[List["FormulaDetail"]] = Relationship(
        back_populates="formula",
        sa_relationship_kwargs={"lazy": "selectin"}
    )
