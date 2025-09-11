import pytest
from tests.fixtures.hardware_device_fixture import create_hardware_device, HARDWARE_DEVICE
from src.cruds.hardware_device import HardwareDeviceRepository

@pytest.fixture
def hardware_device_repository(session) -> HardwareDeviceRepository:
    return HardwareDeviceRepository(session)

def test_create_hardware_device(session, actor):
    hardware_device = create_hardware_device(session, actor=actor)
    assert hardware_device.id is not None
    assert hardware_device.name == "Dispositivo de Teste"
    assert hardware_device.connection_template_id == 1

def test_update_hardware_device(session, hardware_device_repository, actor):
    hardware_device = create_hardware_device(session, actor=actor)
    updated_device = hardware_device_repository.update(hardware_device.id, {"name": "Dispositivo Atualizado"}, actor)
    assert updated_device.name == "Dispositivo Atualizado"

def test_get_hardware_device(session, hardware_device_repository, actor):
    hardware_device = create_hardware_device(session, actor=actor)
    fetched_device = hardware_device_repository.get(hardware_device.id, actor)
    assert fetched_device.id == hardware_device.id
    assert fetched_device.name == "Dispositivo de Teste"
