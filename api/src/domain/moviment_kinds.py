from typing import List
from sqlmodel import Field, Relationship
from src.domain.base import Base


class MovimentKind(Base, table=True):
    __tablename__ = "moviment_kinds"

    #ENTRADA / SAIDA / TRANSFERENCIA
    kind: str = Field(nullable=False, max_length=100)
    code: str = Field(nullable=True, max_length=255)
