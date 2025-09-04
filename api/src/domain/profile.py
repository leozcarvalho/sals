from typing import List, Optional
from sqlmodel import SQLModel, Field
from sqlalchemy import JSON, Column
from src.domain.base import Base


class Profile(Base, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    permissions: List[str] = Field(
        default_factory=list,
        sa_column=Column(JSON, nullable=False)
    )