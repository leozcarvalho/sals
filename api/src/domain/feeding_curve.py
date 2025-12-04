from sqlmodel import Field, Relationship
from src.domain.base import Base
from typing import Optional, List

class FeedingCurve(Base, table=True):
    __tablename__ = "feeding_curves"

    name: str = Field(nullable=False, max_length=100)
    description: str = Field(nullable=True, max_length=255)
    is_active: bool = Field(nullable=False, default=True)

    details: Optional[List["FeedingCurveDetail"]] = Relationship(
        back_populates="feeding_curve",
        sa_relationship_kwargs={"lazy": "selectin"}
    )

    batch: "Batch" = Relationship(back_populates="feeding_curve")
