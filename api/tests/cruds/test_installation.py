import pytest
from tests.fixtures.hardware_device_fixture import create_hardware_device, HARDWARE_DEVICE, hardware_device_repository
from tests.fixtures.installation_fixture import create_installation, installation_repository, INSTALLATION




def test_create_installation(installation_repository, create_hardware_device):
    hardware_device = create_hardware_device()
    data = INSTALLATION.model_dump()
    data.update({"hardware_device_id": hardware_device.id})
    installation = installation_repository.save(data)
    assert installation.id is not None
    assert installation.device_id == installation.id
    assert installation.hardware_device_id == hardware_device.id