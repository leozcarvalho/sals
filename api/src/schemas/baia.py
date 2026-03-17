from pydantic.main import BaseModel
from typing import Optional, List
from decimal import Decimal
from src.schemas.global_schemas import BaseFilter, GlobalFields
from src.schemas.valves import Valve

class BaiaBase(BaseModel):
    name: str
    sala_id: int
    animals_quantity: Optional[int] = 0
    t1: Optional[Decimal] = Decimal(0.0)
    t2: Optional[Decimal] = Decimal(0.0)
    t3: Optional[Decimal] = Decimal(0.0)
    t4: Optional[Decimal] = Decimal(0.0)
    t5: Optional[Decimal] = Decimal(0.0)
    t6: Optional[Decimal] = Decimal(0.0)

class BaiaCreate(BaiaBase):
    pass

class BaiaUpdate(BaiaBase):
    pass

class Baia(BaiaBase, GlobalFields):
    valvulas: Optional[List[Valve]] = None

class BaiaFilter(BaseFilter):
    name: Optional[str] = None
    sala_id: Optional[int] = None
