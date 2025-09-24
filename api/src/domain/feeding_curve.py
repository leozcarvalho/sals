from sqlmodel import Field
from src.domain.base import Base

class FeedingCurve(Base, table=True):
    __tablename__ = "feeding_curves"

    name: str = Field(nullable=False, max_length=100)
    description: str = Field(nullable=True, max_length=255)
    is_active: bool = Field(nullable=False, default=True)
