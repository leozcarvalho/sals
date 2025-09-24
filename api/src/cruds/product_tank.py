from sqlmodel import Session
from src.cruds.repo import Repository
from src.domain.product_tank import ProductTank
from src.cruds.device_pins import DevicePinRepository

class ProductTankRepository(Repository):
    def __init__(self, db_session: Session):
        super().__init__(ProductTank, db_session)
        self.device_pin_repo = DevicePinRepository(db_session)

    def save(self, values, actor=None):
        self.device_pin_repo._is_valid_pin(values["pin_id"])
        return super().save(values, actor)
    
    def update(self, id, values, actor=None):
        self.device_pin_repo._is_valid_pin(values["pin_id"])
        return super().update(id, values, actor)