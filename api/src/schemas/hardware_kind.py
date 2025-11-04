from pydantic.main import BaseModel
from typing import Optional
from src.schemas.global_schemas import BaseFilter, GlobalFields

class HardwareKindBase(BaseModel):
    name: str
    kind: str


class HardwareKindCreate(HardwareKindBase):
    pass

class HardwareKindUpdate(HardwareKindBase):
    pass

class HardwareKind(HardwareKindBase, GlobalFields):
    pass

class HardwareKindFilter(BaseFilter):
    kind: Optional[str] = None
