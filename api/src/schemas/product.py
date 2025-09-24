from pydantic.main import BaseModel
from typing import Optional
from src.schemas.global_schemas import BaseFilter, GlobalFields

class ProductBase(BaseModel):
    name: str
    description: Optional[str] = None
    moisture_percentage: int
    kind: str
    density: int
    is_active: bool = True

class ProductCreate(ProductBase):
    pass

class ProductUpdate(ProductBase):
    pass

class ProductRead(ProductBase, GlobalFields):
    pass

class ProductFilter(BaseFilter):
    pass