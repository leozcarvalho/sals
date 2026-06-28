from sqlalchemy.orm import Session
from src.domain.receita import Receita
from src.cruds.repo import Repository


class ReceitaRepository(Repository):
    def __init__(self, session: Session):
        super().__init__(Receita, session)
