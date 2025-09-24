from pydantic.main import BaseModel
from src.schemas.global_schemas import BaseFilter, GlobalFields

class FormulaDetailBase(BaseModel):
    product_id: int
    product_percentage_without_moisture: int

class FormulaDetailCreate(FormulaDetailBase):
    pass

class FormulaDetailUpdate(FormulaDetailBase):
    pass

class FormulaDetailRead(FormulaDetailBase, GlobalFields):
    formula_id: int

class FormulaDetFilter(BaseFilter):
    pass
