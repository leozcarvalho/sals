from sqlalchemy.orm import Session
from src.domain.receita_distribuicao import ReceitaDistribuicao
from src.cruds.repo import Repository


class ReceitaDistribuicaoRepository(Repository):
    def __init__(self, session: Session):
        super().__init__(ReceitaDistribuicao, session)

    def get_by_receita(self, receita_id: int) -> list[ReceitaDistribuicao]:
        return self.get_list(filters={"receita_id": receita_id}, order_by={"baia_id": "asc"})
