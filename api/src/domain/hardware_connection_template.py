from typing import Optional, List
from sqlmodel import Field, Relationship
from src.domain.base import Base

class ConnectionTemplate(Base, table=True):
    __tablename__ = "connection_templates"

    name: str = Field(nullable=False, max_length=255, unique=True)
    template_url: str = Field(nullable=False, max_length=1000)
    query_string: str = Field(default="")
    devices: List["Device"] = Relationship(back_populates="connection_template")
