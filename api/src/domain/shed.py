from typing import List, Optional
from sqlmodel import Field, Relationship
from src.domain.base import Base

class Shed(Base, table=True):
    __tablename__ = "sheds"

    name: str = Field(nullable=False, max_length=100)

    rooms: List["ShedRoom"] = Relationship(back_populates="shed")
