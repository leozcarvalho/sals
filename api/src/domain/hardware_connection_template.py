from typing import Optional, List
from sqlmodel import Field, Relationship
from src.domain.base import Base


class ConnectionTemplate(Base, table=True):
    __tablename__ = "connection_templates"

    name: str = Field(nullable=False, max_length=255)
    template_url: str = Field(nullable=False, max_length=1000)

    # Relacionamento inverso
    devices: List["Device"] = Relationship(back_populates="connection_template")
