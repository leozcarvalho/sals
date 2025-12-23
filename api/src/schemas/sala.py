from pydantic.main import BaseModel
from typing import Optional, List
from src.schemas.global_schemas import BaseFilter, GlobalFields
from src.schemas.device_pins import DevicePin
from src.schemas.baia import Baia


class SalaBase(BaseModel):
    name: str
    shed_id: int
    entrance_pin_id: Optional[int] = None

class SalaCreate(SalaBase):
    pass

class SalaUpdate(SalaBase):
    pass

class Sala(SalaBase, GlobalFields):
    entrance_pin: Optional[DevicePin] = None
    baias: Optional[List[Baia]] = None

class SalaFilter(BaseFilter):
    name: Optional[str] = None
    shed_id: Optional[int] = None
    #filtro pra saber se ta no lote
    is_in_batch: Optional[bool] = None