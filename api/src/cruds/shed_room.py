from sqlalchemy.orm import Session
from src.domain import ShedRoom, Batch
from src.cruds.repo import Repository

#Salas
class ShedRoomRepository(Repository):
    def __init__(self, session: Session):
        super().__init__(ShedRoom, session)
    
    def build_filter(self, query, filters):
        if filters.get("is_in_batch") is not None:
            is_in_batch = filters.pop("is_in_batch")
            if is_in_batch:
                query = query.join(Batch, Batch.shed_room_id == ShedRoom.id)
            else:
                query = query.outerjoin(Batch, Batch.shed_room_id == ShedRoom.id).filter(Batch.id == None)
        return super().build_filter(query, filters)
