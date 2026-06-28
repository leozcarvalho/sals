from datetime import date, time, datetime
from decimal import Decimal
from typing import Optional
from pydantic import BaseModel, ConfigDict
from src.domain.receita import ReceitaStatus
from src.schemas.global_schemas import BaseFilter, GlobalFields


class ReceitaRead(GlobalFields):
    data: date
    seq: int
    id_cz: int
    id_fo: int
    trato: int
    etapa: int
    p_etapa_s_frac: Decimal
    hora_trato: time
    h_inicio: Optional[datetime] = None
    h_fim: Optional[datetime] = None
    status: ReceitaStatus

    model_config = ConfigDict(from_attributes=True)


class ReceitaFilter(BaseFilter):
    data: Optional[date] = None
    id_cz: Optional[int] = None
    status: Optional[ReceitaStatus] = None
