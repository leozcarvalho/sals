from sqlalchemy.orm import Session
from src.domain import ConnectionTemplate
from src.cruds.repo import Repository

class HardwareConnectionTemplateRepository(Repository):
    def __init__(self, session: Session):
        super().__init__(ConnectionTemplate, session)
