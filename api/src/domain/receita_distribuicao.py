import enum
from typing import Optional
from datetime import datetime
from decimal import Decimal
from sqlmodel import Field, Relationship
from sqlalchemy import Column, Numeric, Enum as SAEnum
from src.domain.base import Base


class ReceitaDistribuicaoStatus(str, enum.Enum):
    aguardando   = "aguardando"
    distribuir   = "distribuir"
    distribuindo = "distribuindo"
    distribuido  = "distribuido"
    cancelado    = "cancelado"


class ReceitaDistribuicao(Base, table=True):
    __tablename__ = "receitas_distribuicao"

    receita_id:              int            = Field(foreign_key="receitas.id",  nullable=False)
    cozinha_id:              int            = Field(foreign_key="kitchens.id",  nullable=False)
    galpao_id:               int            = Field(foreign_key="sheds.id",     nullable=False)
    sala_id:                 int            = Field(foreign_key="salas.id",     nullable=False)
    baia_id:                 int            = Field(foreign_key="baias.id",     nullable=False)
    quantidade_suinos:       int            = Field(nullable=False)
    formula_id:              int            = Field(foreign_key="formulas.id",  nullable=False)
    trato_id:                int            = Field(foreign_key="tratos.id",    nullable=False)
    etapa:                   int            = Field(nullable=False)
    peso_sem_fracao_liquida: Decimal        = Field(sa_column=Column(Numeric(10, 2)))
    h_inicio:                Optional[datetime] = Field(default=None, nullable=True)
    h_fim:                   Optional[datetime] = Field(default=None, nullable=True)
    status: ReceitaDistribuicaoStatus = Field(
        sa_column=Column(
            SAEnum(ReceitaDistribuicaoStatus, name="receita_distribuicao_status"),
            nullable=False,
            default=ReceitaDistribuicaoStatus.aguardando,
        )
    )

    receita: Optional["Receita"] = Relationship(
        sa_relationship_kwargs={"foreign_keys": "[ReceitaDistribuicao.receita_id]"}
    )
    baia: Optional["Baia"] = Relationship(
        sa_relationship_kwargs={"foreign_keys": "[ReceitaDistribuicao.baia_id]"}
    )
