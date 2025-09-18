from typing import Optional, List
from sqlmodel import Field, Relationship
from src.domain.base import Base

class HealthcheckPriority(Base, table=True):
    __tablename__ = "healthcheck_priorities"

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(nullable=False, max_length=100)
    interval_milliseconds: int = Field(nullable=False)

    installations: List["Installation"] = Relationship(back_populates="healthcheck_priority")
