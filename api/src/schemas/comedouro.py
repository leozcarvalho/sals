from pydantic.main import BaseModel
from typing import Optional, List
from src.schemas.global_schemas import BaseFilter, GlobalFields
from src.schemas.device_pins import DevicePin

class ComedouroBase(BaseModel):
    name: str
    baia_id: int
    max_weight: Optional[float] = None

class ComedouroCreate(ComedouroBase):
    pass

class ComedouroUpdate(ComedouroBase):
    pass

class Comedouro(ComedouroBase, GlobalFields):
    pass

class ComedouroFilter(BaseFilter):
    name: Optional[str] = None
    baia_id: Optional[int] = None
