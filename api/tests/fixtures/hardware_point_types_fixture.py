import pytest
from src.cruds.hardware_point_types import HardwarePointTypeRepository
from src.schemas.hardware_point_types import HardwarePointTypeCreate

@pytest.fixture
def hardware_point_type_repository(session) -> HardwarePointTypeRepository:
    return HardwarePointTypeRepository(session)

HARDWARE_POINT_TYPE = HardwarePointTypeCreate(
    points_quantity=32,
    kind="bit",
)

@pytest.fixture
def create_hardware_point_type(hardware_point_type_repository: HardwarePointTypeRepository, actor):
    def _create_hardware_point_type(**overrides):
        hardware_point_type_dict = HARDWARE_POINT_TYPE.model_dump()
        hardware_point_type_dict.update(overrides)
        hardware_point_type = HardwarePointTypeCreate(**hardware_point_type_dict)
        hardware_point_type = hardware_point_type_repository.save(hardware_point_type.model_dump(), actor=actor)
        return hardware_point_type
    return _create_hardware_point_type
