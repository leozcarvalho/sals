from sqlalchemy.orm import Session
from src.domain.shed import Shed
from src.cruds.repo import Repository

class ShedRepository(Repository):
    def __init__(self, session: Session):
        super().__init__(Shed, session)
