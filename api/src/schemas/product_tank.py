from decimal import Decimal
from pydantic.main import BaseModel
from typing import Optional
from src.schemas.global_schemas import BaseFilter, GlobalFields
from src.schemas.product import ProductRead
from src.schemas.device_pins import DevicePin

class ProductTankBase(BaseModel):
    name: str
    description: Optional[str] = None
    screw_pin_id: Optional[int] = None
    product_id: Optional[int] = None
    volume: Decimal
    is_dosador_seco: bool = False
    scale_pin_id: Optional[int] = None

class ProductTankCreate(ProductTankBase):
    pass

class ProductTankUpdate(ProductTankBase):
    pass

class ProductTankRead(ProductTankBase, GlobalFields):
    product: Optional[ProductRead]
    screw_pin: Optional[DevicePin]
    scale_pin: Optional[DevicePin]

class ProductTankFilter(BaseFilter):
    pass