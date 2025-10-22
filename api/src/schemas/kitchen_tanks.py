from pydantic.main import BaseModel
from typing import Optional
from src.schemas.global_schemas import BaseFilter, GlobalFields
from src.schemas.product_tank import ProductTankRead

class KitchenTankBase(BaseModel):
    product_tank_id: int

class KitchenTankCreate(KitchenTankBase):
    pass

class KitchenTankUpdate(KitchenTankBase):
    pass

class KitchenTank(KitchenTankBase, GlobalFields):
    kitchen_id: int
    tank: Optional[ProductTankRead] = None

class KitchenTankFilter(BaseFilter):
    product_tank_id: Optional[int] = None