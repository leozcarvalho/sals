from pydantic.main import BaseModel
from typing import Optional, List
from src.schemas.global_schemas import BaseFilter, GlobalFields
from src.schemas.device_pins import DevicePin
from src.schemas.kitchen_tanks import KitchenTank, KitchenTankCreate
from pydantic import field_validator
from src.adapters import utils
class KitchenBase(BaseModel):
    name: str
    shaker_pin_id: int
    pump_pin_id: int
    scale_pin_id: int   
    max_bowl_weight: float
    bowl_weight_fraction: float

    @field_validator("bowl_weight_fraction")
    def validate_bowl_weight_fraction(cls, v):
        return utils.range_validator(v, 0, 100)

class KitchenCreate(KitchenBase):
    tanks: Optional[List[KitchenTankCreate]] = []

class KitchenUpdate(KitchenBase):
    tanks: Optional[List[KitchenTankCreate]] = []

class Kitchen(KitchenBase, GlobalFields):
    shaker_pin: DevicePin
    pump_pin: DevicePin
    scale_pin: DevicePin
    tanks: Optional[list[KitchenTank]] = []

class KitchenFilter(BaseFilter):
    name: Optional[str] = None
