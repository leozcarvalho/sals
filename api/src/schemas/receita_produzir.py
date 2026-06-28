from datetime import datetime
from decimal import Decimal
from typing import Optional
from pydantic import ConfigDict
from src.domain.receita_produzir import ReceitaProduzirStatus
from src.schemas.global_schemas import GlobalFields


class ReceitaProduzirRead(GlobalFields):
    receita_id:                    int
    cozinha_id:                    int
    formula_id:                    int
    trato_id:                      int
    etapa:                         int
    produto_id:                    int
    seq_dosagem:                   int
    peso_etapa_sem_fracao_liquida: Decimal
    peso_etapa_com_fracao_liquida: Decimal
    volume_etapa:                  Decimal
    produto_e_agua:                bool
    h_inicio:                      Optional[datetime] = None
    h_fim:                         Optional[datetime] = None
    status:                        ReceitaProduzirStatus

    model_config = ConfigDict(from_attributes=True)
