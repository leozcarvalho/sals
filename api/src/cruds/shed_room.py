from sqlalchemy.orm import Session
from src.domain.shed_room import ShedRoom
from src.cruds.repo import Repository

class ShedRoomRepository(Repository):
    def __init__(self, session: Session):
        super().__init__(ShedRoom, session)
