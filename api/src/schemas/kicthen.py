from pydantic.main import BaseModel
from typing import Optional
from src.schemas.global_schemas import BaseFilter, GlobalFields
from src.schemas.device_pins import DevicePin

class KitchenBase(BaseModel):
    name: str
    shaker_pin_id: int
    pump_pin_id: int
    scale_pin_id: int
    product_pin_id: int


class KitchenCreate(KitchenBase):
    pass

class KitchenUpdate(KitchenBase):
    pass

class Kitchen(KitchenBase, GlobalFields):
    shaker_pin: DevicePin
    pump_pin: DevicePin
    scale_pin: DevicePin
    product_pin: DevicePin

class KitchenFilter(BaseFilter):
    kind: Optional[str] = None
