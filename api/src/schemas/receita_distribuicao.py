from datetime import datetime
from decimal import Decimal
from typing import Optional
from pydantic import ConfigDict
from src.domain.receita_distribuicao import ReceitaDistribuicaoStatus
from src.schemas.global_schemas import GlobalFields


class ReceitaDistribuicaoRead(GlobalFields):
    receita_id:              int
    cozinha_id:              int
    galpao_id:               int
    sala_id:                 int
    baia_id:                 int
    quantidade_suinos:       int
    formula_id:              int
    trato_id:                int
    etapa:                   int
    peso_sem_fracao_liquida: Decimal
    h_inicio:                Optional[datetime] = None
    h_fim:                   Optional[datetime] = None
    status:                  ReceitaDistribuicaoStatus

    model_config = ConfigDict(from_attributes=True)
