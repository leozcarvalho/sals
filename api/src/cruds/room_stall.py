from sqlalchemy.orm import Session
from src.domain.room_stall import RoomStall
from src.cruds.repo import Repository

class RoomStallRepository(Repository):
    def __init__(self, session: Session):
        super().__init__(RoomStall, session)
