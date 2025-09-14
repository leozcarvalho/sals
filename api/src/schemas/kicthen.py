from pydantic.main import BaseModel
from typing import Optional, List
from src.schemas.global_schemas import BaseFilter, GlobalFields
from src.schemas.device_pins import DevicePin
from src.schemas.kitchen_products import KitchenProduct, KitchenProductCreate

class KitchenBase(BaseModel):
    name: str
    shaker_pin_id: int
    pump_pin_id: int
    scale_pin_id: int

class KitchenCreate(KitchenBase):
    products: Optional[List[KitchenProductCreate]] = []

class KitchenUpdate(KitchenBase):
    products: Optional[List[KitchenProductCreate]] = []

class Kitchen(KitchenBase, GlobalFields):
    shaker_pin: DevicePin
    pump_pin: DevicePin
    scale_pin: DevicePin
    products: Optional[list[KitchenProduct]] = []

class KitchenFilter(BaseFilter):
    kind: Optional[str] = None
