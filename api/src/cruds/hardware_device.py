from sqlalchemy.orm import Session
from src.domain.hardware_device import Device
from src.cruds.repo import Repository

class HardwareDeviceRepository(Repository):
    def __init__(self, session: Session):
        super().__init__(Device, session)