from sqlalchemy.orm import Session
from src.cruds.repo import Repository
from src.domain import Batch
from src.cruds.moviment import MovimentRepository

class BatchRepository(Repository):
    def __init__(self, session: Session):
        super().__init__(Batch, session)
        self.moviment_repo = MovimentRepository(session)

    def exec_batch_moviment(self, batch_id: int, moviment_data: dict, actor=None):
        moviment_data['batch_id'] = batch_id
        return self.moviment_repo.save(moviment_data, actor)

    def __update_moviments(self, batch_id: int, moviments_data, actor=None):
        for moviment_data in moviments_data:
            self.exec_batch_moviment(batch_id, moviment_data, actor)

    def save(self, values, actor=None):
        moviments = values.pop('moviments', None) or []
        batch = super().save(values, actor)
        self.__update_moviments(batch.id, moviments, actor)
        return batch

    def update(self, id, values, actor=None):
        moviments = values.pop('moviments', None) or []
        return super().update(id, values, actor)