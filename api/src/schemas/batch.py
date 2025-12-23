from pydantic.main import BaseModel
from typing import Optional, List
from src.schemas.global_schemas import BaseFilter, GlobalFields
from src.schemas.shed import Shed
from src.schemas.sala import Sala
from src.schemas.feeding_curve import FeedingCurve
from src.schemas.moviment import Moviment, MovimentCreate


class BatchBase(BaseModel):
    name: str
    description: Optional[str] = None
    initial_day: int
    is_active: Optional[bool] = True
    feeding_curve_id: int
    shed_id: int
    sala_id: int
    moviments: Optional[List[MovimentCreate]] = None

class BatchCreate(BatchBase):
    pass

class BatchUpdate(BatchBase):
    pass

class Batch(BatchBase, GlobalFields):
    shed: Optional[Shed] = None
    sala: Optional[Sala] = None
    feeding_curve: Optional[FeedingCurve] = None
    moviments: Optional[list[Moviment]] = None

class BatchFilter(BaseFilter):
    pass
