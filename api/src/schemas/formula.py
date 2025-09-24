from pydantic.main import BaseModel
from typing import Optional, List
from src.schemas.global_schemas import BaseFilter, GlobalFields
from src.schemas.formula_detail import FormulaDetailCreate, FormulaDetailUpdate, FormulaDetailRead

class FormulaBase(BaseModel):
    name: str
    description: Optional[str] = None
    water_percentage: int
    stirring_time: int
    is_active: bool = True

class FormulaCreate(FormulaBase):
    details: Optional[List[FormulaDetailCreate]] = None

class FormulaUpdate(FormulaBase):
    details: Optional[List[FormulaDetailUpdate]] = None

class FormulaRead(FormulaBase, GlobalFields):
    details: List[FormulaDetailRead] = []

class FormulaFilter(BaseFilter):
    pass
