from pydantic.main import BaseModel
from decimal import Decimal
from pydantic import field_validator
from typing import Optional, List

from src.schemas.global_schemas import BaseFilter, GlobalFields
from src.schemas.device_pins import DevicePin
from src.schemas.kicthen import Kitchen
from src.adapters import utils

class DosadorSecoBase(BaseModel):
    name: str
    output_pin_id: Optional[int] = None
    scale_pin_id: Optional[int] = None
    volume_misturador: Decimal
    destiny_kitchen_id: Optional[int] = None
    fracao_volume_misturador: Decimal
    ignore_kitchen_weight: bool = False

    @field_validator("fracao_volume_misturador")
    def validate_fracao_volume_misturador(cls, v):
        return utils.range_validator(v, 0, 100)

class DosadorSecoCreate(DosadorSecoBase):
    pass

class DosadorSecoUpdate(DosadorSecoBase):
    pass

class DosadorSeco(DosadorSecoBase, GlobalFields):
    output_pin: Optional[DevicePin] = None
    scale_pin: Optional[DevicePin] = None
    destiny_kitchen: Optional[Kitchen] = None

class DosadorSecoFilter(BaseFilter):
    name: Optional[str] = None
