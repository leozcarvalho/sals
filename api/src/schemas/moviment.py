from pydantic.main import BaseModel
from typing import Optional
from src.schemas.global_schemas import BaseFilter, GlobalFields


class MovimentBase(BaseModel):
    id: Optional[int] = None
    moviment_kind_id: int
    stall_origin_id: Optional[int] = None
    stall_destination_id: Optional[int] = None
    quantity: Optional[int] = None
    description: Optional[str] = None

class MovimentCreate(MovimentBase):
    pass

class MovimentUpdate(MovimentBase):
    pass

class Moviment(MovimentBase, GlobalFields):
    batch_id: int

class MovimentFilter(BaseFilter):
    batch_id: Optional[int] = None
    moviment_kind_id: Optional[int] = None
    stall_origin_id: Optional[int] = None
    stall_destination_id: Optional[int] = None

