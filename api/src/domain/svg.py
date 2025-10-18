from typing import List, Optional
from sqlmodel import Field, Relationship
from src.domain.base import Base

class SVG(Base, table=True):
    __tablename__ = "svgs"

    name: str = Field(nullable=False, max_length=100)
    owner_type: str = Field(nullable=False, max_length=50)  # Ex: 'shed', 'kitchen', 'board'
    owner_id: int = Field(nullable=False)  # ID do registro correspondente
    content: str = Field(nullable=False, max_length=5000)
