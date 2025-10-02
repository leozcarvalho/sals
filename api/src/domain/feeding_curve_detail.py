from sqlmodel import Field, Relationship
from src.domain.base import Base
from typing import Optional

class FeedingCurveDetail(Base, table=True):
    __tablename__ = "feeding_curve_details"

    feeding_curve_id: int = Field(foreign_key="feeding_curves.id", nullable=False)
    age_day: int = Field(nullable=False)
    formula_id: int = Field(foreign_key="formulas.id", nullable=False)
    formula_mass: float = Field(nullable=False, ge=0)
    is_active: bool = Field(nullable=False, default=True)

    feeding_curve: Optional["FeedingCurve"] = Relationship(
        back_populates="details",
        sa_relationship_kwargs={"lazy": "selectin"}
    )
