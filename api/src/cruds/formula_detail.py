from sqlmodel import Session
from src.cruds.repo import Repository
from src.domain.formula_detail import FormulaDetail

class FormulaDetailRepository(Repository):
    def __init__(self, db_session: Session):
        super().__init__(FormulaDetail, db_session)

    def delete_by_formula_id(self, formula_id: int):
        self.db_session.query(FormulaDetail).filter(FormulaDetail.formula_id == formula_id).delete()
