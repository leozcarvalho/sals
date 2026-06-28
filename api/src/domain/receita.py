import enum
from typing import Optional
from datetime import date, time, datetime
from decimal import Decimal
from sqlmodel import Field, Relationship
from sqlalchemy import Column, Numeric, Enum as SAEnum
from src.domain.base import Base


class ReceitaStatus(str, enum.Enum):
    aguardando = "aguardando"
    produzir = "produzir"
    produzindo = "produzindo"
    produzido = "produzido"
    cancelada = "cancelada"


class Receita(Base, table=True):
    __tablename__ = "receitas"

    data: date = Field(nullable=False)
    seq: int = Field(nullable=False)
    id_cz: int = Field(foreign_key="kitchens.id", nullable=False)
    id_fo: int = Field(foreign_key="formulas.id", nullable=False)
    trato: int = Field(foreign_key="tratos.id", nullable=False)
    etapa: int = Field(nullable=False)
    p_etapa_s_frac: Decimal = Field(sa_column=Column(Numeric(10, 2)))
    hora_trato: time = Field(nullable=False)
    h_inicio: Optional[datetime] = Field(default=None, nullable=True)
    h_fim: Optional[datetime] = Field(default=None, nullable=True)
    status: ReceitaStatus = Field(
        sa_column=Column(
            SAEnum(ReceitaStatus, name="receita_status"),
            nullable=False,
            default=ReceitaStatus.aguardando,
        )
    )

    cozinha: Optional["Kitchen"] = Relationship(
        sa_relationship_kwargs={"foreign_keys": "[Receita.id_cz]"}
    )
    formula: Optional["Formula"] = Relationship(
        sa_relationship_kwargs={"foreign_keys": "[Receita.id_fo]"}
    )
    trato_rel: Optional["Trato"] = Relationship(
        sa_relationship_kwargs={"foreign_keys": "[Receita.trato]"}
    )
