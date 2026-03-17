from pydantic.main import BaseModel
from typing import Optional, List
from decimal import Decimal
from src.schemas.global_schemas import BaseFilter, GlobalFields
from src.schemas.device_pins import DevicePin
from src.schemas.kitchen_tanks import KitchenTank, KitchenTankCreate
from pydantic import field_validator
from src.adapters import utils

class KitchenBase(BaseModel):
    name: str
    shaker_pin_id: Optional[int] = None
    pump_pin_id: Optional[int] = None
    scale_pin_id: Optional[int] = None
    volume_misturador: Decimal
    fracao_volume_misturador: Decimal

    @field_validator("fracao_volume_misturador")
    def validate_fracao_volume_misturador(cls, v):
        return utils.range_validator(v, 0, 100)

class KitchenCreate(KitchenBase):
    tanks: Optional[List[KitchenTankCreate]] = []

class KitchenUpdate(KitchenBase):
    tanks: Optional[List[KitchenTankCreate]] = []

class Kitchen(KitchenBase, GlobalFields):
    shaker_pin: Optional[DevicePin] = None
    pump_pin: Optional[DevicePin] = None
    scale_pin: Optional[DevicePin] = None
    tanks: Optional[list[KitchenTank]] = []

class KitchenFilter(BaseFilter):
    name: Optional[str] = None
