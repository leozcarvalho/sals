from typing import List
from sqlalchemy.orm import Session
from src.domain.moviment_kinds import MovimentKind
from src.cruds.repo import Repository

class MovimentKindRepository(Repository):
    def __init__(self, session: Session):
        super().__init__(MovimentKind, session)
