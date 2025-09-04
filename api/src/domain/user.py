from typing import ClassVar

from sqlmodel import Field, Relationship
from src.domain.base import Base

class User(Base, table=True):
    email: str = Field(index=True, unique=True, nullable=False)
    name: str
    password: str
    is_active: bool = Field(default=True)
    profile_id: int = Field(foreign_key="profile.id")

    exhibition_name: ClassVar[str] = "Usuário"
