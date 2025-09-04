import pytest
from .hardware_kind_fixture import create_hardware_kind
from .hardware_point_types_fixture import create_hardware_point_type
from tests.fixtures.hardware_connection_template_fixture import create_hardware_connection_template

from src.cruds.hardware_device import HardwareDeviceRepository
from src.schemas.hardware_device import HardwareDeviceCreate

@pytest.fixture
def hardware_device_repository(session) -> HardwareDeviceRepository:
    return HardwareDeviceRepository(session)

HARDWARE_DEVICE = HardwareDeviceCreate(
    name="Dispositivo de Teste",
    connection_template_id=1,
    hardware_kind_id=1,
    point_type_id=1,
    svg_template="<svg></svg>"
)

@pytest.fixture()
def create_hardware_device(hardware_device_repository: HardwareDeviceRepository, actor):
    def _create_hardware_device(**overrides):
        hardware_device_dict = HARDWARE_DEVICE.model_dump()
        hardware_device_dict.update(overrides)
        hardware_device = HardwareDeviceCreate(**hardware_device_dict)
        hardware_device = hardware_device_repository.save(hardware_device.model_dump(), actor=actor)
        return hardware_device
    return _create_hardware_device
