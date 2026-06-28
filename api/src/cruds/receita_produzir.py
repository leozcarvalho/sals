from sqlalchemy.orm import Session
from src.domain.receita_produzir import ReceitaProduzir
from src.cruds.repo import Repository


class ReceitaProduzirRepository(Repository):
    def __init__(self, session: Session):
        super().__init__(ReceitaProduzir, session)

    def get_by_receita(self, receita_id: int) -> list[ReceitaProduzir]:
        return self.get_list(filters={"receita_id": receita_id}, order_by={"seq": "asc"})
