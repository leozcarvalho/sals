from sqlmodel import Session
from src.cruds.repo import Repository
from src.domain.formula import Formula
from src.cruds.formula_detail import FormulaDetailRepository
from src.schemas.formula_detail import FormulaDetailCreate
from typing import List

class FormulaRepository(Repository):
    def __init__(self, db_session: Session):
        super().__init__(Formula, db_session)
        self.formula_details_repo = FormulaDetailRepository(db_session)
    
    def save(self, values, actor=None):
        details = values.pop('details', [])
        formula = super().save(values, actor)
        self.__update_details(formula.id, details, actor)
        return formula
    
    def update(self, id, values, actor=None):
        details = values.pop('details', [])
        formula = super().update(id, values, actor)
        self.__update_details(formula.id, details, actor)
        return formula

    def __update_details(self, formula_id: int, details: List[FormulaDetailCreate], actor=None):
        self.formula_details_repo.delete_by_formula_id(formula_id)
        for detail in details:
            values = dict(
                formula_id=formula_id,
                product_id=detail['product_id'],
                product_percentage_without_moisture=detail['product_percentage_without_moisture']
            )
            self.formula_details_repo.save(values, actor)
