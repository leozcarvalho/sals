from sqlmodel import Session
from src.cruds.repo import Repository
from src.domain.kitchen_tanks import KitchenTank

class KitchenTankRepository(Repository):
    def __init__(self, db_session: Session):
        super().__init__(KitchenTank, db_session)

    def delete_by_kitchen_id(self, kitchen_id: int):
        self.db_session.query(KitchenTank).filter(KitchenTank.kitchen_id == kitchen_id).delete()
