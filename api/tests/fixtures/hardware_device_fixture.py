import pytest
from src.cruds.hardware_device import HardwareDeviceRepository
from src.schemas.hardware_device import HardwareDeviceCreate

HARDWARE_DEVICE = HardwareDeviceCreate(
    name="Dispositivo de Teste",
    connection_template_id=1,
    hardware_kind_id=1,
    point_type_id=1,
)

def create_hardware_device(
    session,
    actor=None,
    **overrides,
):
    repo = HardwareDeviceRepository(session)
    hardware_device_dict = HARDWARE_DEVICE.model_dump()
    hardware_device_dict.update(overrides)
    hardware_device = HardwareDeviceCreate(**hardware_device_dict)
    hardware_device = repo.save(hardware_device.model_dump(), actor=actor)
    return hardware_device
