from pydantic.main import BaseModel
from typing import Optional
from src.schemas.global_schemas import BaseFilter, GlobalFields
from src.schemas.product import ProductRead
from src.schemas.device_pins import DevicePin

class ProductTankBase(BaseModel):
    name: str
    description: Optional[str] = None
    pin_id: int
    product_id: int

class ProductTankCreate(ProductTankBase):
    pass

class ProductTankUpdate(ProductTankBase):
    pass

class ProductTankRead(ProductTankBase, GlobalFields):
    product: ProductRead
    device_pin: DevicePin

class ProductTankFilter(BaseFilter):
    pass