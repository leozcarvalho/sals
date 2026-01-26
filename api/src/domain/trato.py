from typing import List, Optional
from sqlmodel import Field, Relationship
from src.domain.base import Base
from decimal import Decimal
from sqlalchemy import Column, Numeric

class Trato(Base, table=True):
    __tablename__ = "tratos"

    name: str = Field(nullable=False, max_length=2)
    hour: int = Field(nullable=False)
    percent: Decimal = Field(sa_column=Column(Numeric(5, 2))) # 0 a 100
