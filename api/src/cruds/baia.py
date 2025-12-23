from sqlalchemy.orm import Session
from src.domain.baia import Baia
from src.cruds.repo import Repository

class BaiaRepository(Repository):
    def __init__(self, session: Session):
        super().__init__(Baia, session)
