from sqlalchemy.orm import Session
from src.cruds.repo import Repository
from src.domain import Batch, MovimentKind, ShedRoom
from src.cruds.moviment import MovimentRepository
from src.schemas.moviment import MovimentCreate

class BatchRepository(Repository):
    def __init__(self, session: Session):
        super().__init__(Batch, session)
        self.moviment_repo = MovimentRepository(session)

    def __update_moviments(self, batch_id: int, moviments_data, actor=None):
        moviments_to_save = [ m for m in moviments_data if not m.get('id') ]
        for moviment_data in moviments_to_save:
            moviment_data['batch_id'] = batch_id
            self.moviment_repo.save(moviment_data, actor)
    
    def save(self, values, actor=None):
        moviments = values.pop('moviments', None) or []
        batch = super().save(values, actor)
        self.__update_moviments(batch.id, moviments, actor)
        return batch

    def update(self, id, values, actor=None):
        moviments = values.pop('moviments', None) or []
        self.__update_moviments(id, moviments, actor)
        return super().update(id, values, actor)