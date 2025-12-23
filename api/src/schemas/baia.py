from pydantic.main import BaseModel
from typing import Optional
from src.schemas.global_schemas import BaseFilter, GlobalFields
from src.schemas.comedouro import Comedouro

class BaiaBase(BaseModel):
    name: str
    sala_id: int
    animals_quantity: Optional[int] = 0

class BaiaCreate(BaiaBase):
    pass

class BaiaUpdate(BaiaBase):
    pass

class Baia(BaiaBase, GlobalFields):
    comedouros: Optional[list[Comedouro]] = None

class BaiaFilter(BaseFilter):
    name: Optional[str] = None
    sala_id: Optional[int] = None
