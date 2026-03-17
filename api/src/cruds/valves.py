from sqlalchemy.orm import Session
from src.cruds.repo import Repository
from src.domain.valves import Valve
from src.cruds.device_pins import DevicePinRepository
from src.domain import exceptions as exc

class ValveRepository(Repository):
    def __init__(self, session: Session):
        super().__init__(Valve, session)
        self.device_pin_repo = DevicePinRepository(session)

    def save(self, values, actor=None):
        if values.get("device_pin_id"): self.device_pin_repo._is_valid_pin(values.get("device_pin_id"))
        return super().save(values, actor)

    def update(self, id: int, values, actor=None):
        if values.get("device_pin_id"): self.device_pin_repo._is_valid_pin(values.get("device_pin_id"))
        return super().update(id, values, actor)
