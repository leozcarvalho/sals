from sqlalchemy.orm import Session
from src.domain import HealthcheckPriority
from src.cruds.repo import Repository

class HealthcheckPriorityRepository(Repository):
    def __init__(self, session: Session):
        super().__init__(HealthcheckPriority, session)
