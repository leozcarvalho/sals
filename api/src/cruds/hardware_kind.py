from sqlalchemy.orm import Session
from src.domain import HardwareKind
from src.cruds.repo import Repository

class HardwareKindRepository(Repository):
    def __init__(self, session: Session):
        super().__init__(HardwareKind, session)