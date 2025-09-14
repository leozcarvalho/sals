from pydantic.main import BaseModel
from typing import Optional
from src.schemas.global_schemas import BaseFilter, GlobalFields

class KitchenProductBase(BaseModel):
    device_pin_id: int

class KitchenProductCreate(KitchenProductBase):
    pass

class KitchenProductUpdate(KitchenProductBase):
    pass

class KitchenProduct(KitchenProductBase, GlobalFields):
    kitchen_id: int

class KitchenProductFilter(BaseFilter):
    device_pin_id: Optional[int] = None