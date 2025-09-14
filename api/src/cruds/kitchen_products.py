from sqlmodel import Session
from src.cruds.repo import Repository
from src.domain.kitchen_products import KitchenProduct

class KitchenProductRepository(Repository):
    def __init__(self, db_session: Session):
        super().__init__(KitchenProduct, db_session)

    def delete_by_kitchen_id(self, kitchen_id: int):
        self.db_session.query(KitchenProduct).filter(KitchenProduct.kitchen_id == kitchen_id).delete()
