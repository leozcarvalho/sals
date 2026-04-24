from sqlmodel import Session
from src.domain.exceptions import InvalidData
from src.cruds.repo import Repository
from src.domain.formula import Formula
from src.cruds.formula_detail import FormulaDetailRepository
from src.cruds.product import ProductRepository
from src.schemas.formula_detail import FormulaDetailCreate
from typing import List

class FormulaRepository(Repository):
    def __init__(self, db_session: Session):
        super().__init__(Formula, db_session)
        self.formula_details_repo = FormulaDetailRepository(db_session)
        self.product_repo = ProductRepository(db_session)

    def save(self, values, actor=None):
        details = values.pop('details', None)
        formula = super().save(values, actor)
        if details: self.__update_details(formula.id, details, actor)
        return formula

    def update(self, id, values, actor=None):
        details = values.pop('details', None)
        formula = super().update(id, values, actor)
        if details: self.__update_details(formula.id, details, actor)
        return formula

    def __validate_details(self, details: List[FormulaDetailCreate]):
        total_percentage = 0
        for detail in details:
            product = self.product_repo.get(detail['product_id'])
            pct = detail['product_percentage_without_moisture']

            if product and product.is_micronutrient:
                # Micronutrientes: até 3 casas decimais
                rounded = round(pct, 3)
                if rounded != pct:
                    raise InvalidData(
                        f"Micronutriente '{product.name}': a porcentagem deve ter no máximo 3 casas decimais (recebido: {pct})."
                    )
                continue

            # Produtos convencionais: deve ser inteiro
            if pct != int(pct):
                name = product.name if product else f"ID {detail['product_id']}"
                raise InvalidData(
                    f"Produto '{name}': a porcentagem deve ser um número inteiro (recebido: {pct})."
                )

            total_percentage += pct

        if total_percentage != 100:
            raise InvalidData("A soma das porcentagens dos produtos deve ser igual a 100%.")

    def __update_details(self, formula_id: int, details: List[FormulaDetailCreate], actor=None):
        self.__validate_details(details)
        self.formula_details_repo.delete_by_formula_id(formula_id)
        for detail in details:
            values = dict(
                formula_id=formula_id,
                product_id=detail['product_id'],
                product_percentage_without_moisture=detail['product_percentage_without_moisture']
            )
            self.formula_details_repo.save(values, actor)
