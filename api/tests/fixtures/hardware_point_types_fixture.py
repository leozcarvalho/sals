import pytest
from src.cruds.hardware_point_types import HardwarePointTypeRepository
from src.schemas.hardware_point_types import HardwarePointTypeCreate

HARDWARE_POINT_TYPE = HardwarePointTypeCreate(
    points_quantity=32,
    kind="bit",
)

def create_hardware_point_type(session, actor=None, **overrides):
    repo = HardwarePointTypeRepository(session)
    hardware_point_type_dict = HARDWARE_POINT_TYPE.model_dump()
    hardware_point_type_dict.update(overrides)
    hardware_point_type = HardwarePointTypeCreate(**hardware_point_type_dict)
    hardware_point_type = repo.save(hardware_point_type.model_dump(), actor=actor)
    return hardware_point_type
