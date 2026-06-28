import enum
from typing import Optional
from datetime import datetime
from decimal import Decimal
from sqlmodel import Field, Relationship
from sqlalchemy import Column, Numeric, Enum as SAEnum
from src.domain.base import Base


class ReceitaProduzirStatus(str, enum.Enum):
    aguardando = "aguardando"
    pesar      = "pesar"
    pesando    = "pesando"
    pesado     = "pesado"
    cancelada  = "cancelada"


class ReceitaProduzir(Base, table=True):
    __tablename__ = "receitas_produzir"

    receita_id:                    int            = Field(foreign_key="receitas.id",  nullable=False)
    cozinha_id:                    int            = Field(foreign_key="kitchens.id",  nullable=False)
    formula_id:                    int            = Field(foreign_key="formulas.id",  nullable=False)
    trato_id:                      int            = Field(foreign_key="tratos.id",    nullable=False)
    etapa:                         int            = Field(nullable=False)
    produto_id:                    int            = Field(foreign_key="products.id",  nullable=False)
    seq_dosagem:                   int            = Field(nullable=False)
    peso_etapa_sem_fracao_liquida: Decimal        = Field(sa_column=Column(Numeric(10, 2)))
    peso_etapa_com_fracao_liquida: Decimal        = Field(sa_column=Column(Numeric(10, 2)))
    volume_etapa:                  Decimal        = Field(sa_column=Column(Numeric(10, 2)))
    produto_e_agua:                bool           = Field(default=False, nullable=False)
    h_inicio:                      Optional[datetime] = Field(default=None, nullable=True)
    h_fim:                         Optional[datetime] = Field(default=None, nullable=True)
    status: ReceitaProduzirStatus = Field(
        sa_column=Column(
            SAEnum(ReceitaProduzirStatus, name="receita_produzir_status"),
            nullable=False,
            default=ReceitaProduzirStatus.aguardando,
        )
    )

    receita: Optional["Receita"] = Relationship(
        sa_relationship_kwargs={"foreign_keys": "[ReceitaProduzir.receita_id]"}
    )
    produto: Optional["Product"] = Relationship(
        sa_relationship_kwargs={"foreign_keys": "[ReceitaProduzir.produto_id]"}
    )
