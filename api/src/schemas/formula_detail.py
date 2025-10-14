from pydantic import BaseModel, validator
from src.schemas.global_schemas import BaseFilter, GlobalFields
from src.domain import validators as vd

class FormulaDetailBase(BaseModel):
    product_id: int
    product_percentage_without_moisture: int

    @validator("product_percentage_without_moisture")
    def must_be_positive(cls, v):
        return vd.validate_percent(v, "percentual do produto sem umidade")

class FormulaDetailCreate(FormulaDetailBase):
    pass

class FormulaDetailUpdate(FormulaDetailBase):
    pass

class FormulaDetailRead(FormulaDetailBase, GlobalFields):
    formula_id: int

class FormulaDetFilter(BaseFilter):
    pass
