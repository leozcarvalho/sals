import pytest
from tests.fixtures.hardware_device_fixture import create_hardware_device
from tests.fixtures.account_device_fixture import create_account_device, account_device_repository, ACCOUNT_DEVICE

def test_create_account_device(create_account_device, create_hardware_device):
    account_device = create_account_device()
    assert account_device.id is not None
    assert account_device.name == "Dispositivo de Conta"
    assert account_device.ip_address == "192.168.0.1"