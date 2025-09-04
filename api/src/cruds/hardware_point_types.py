from sqlalchemy.orm import Session
from src.domain.hardware_point_types import PointType
from src.cruds.repo import Repository

class HardwarePointTypeRepository(Repository):
    def __init__(self, session: Session):
        super().__init__(PointType, session)