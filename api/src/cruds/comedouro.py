from sqlalchemy.orm import Session
from src.domain.comedouro import Comedouro
from src.cruds.repo import Repository
from src.cruds.device_pins import DevicePinRepository
from src.cruds.feeder_valves import FeederValveRepository

class ComedouroRepository(Repository):
    def __init__(self, session: Session):
        super().__init__(Comedouro, session)
        self.device_pin_repo = DevicePinRepository(session)
        self.feeder_valve_repo = FeederValveRepository(session)

