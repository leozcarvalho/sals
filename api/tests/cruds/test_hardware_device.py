import pytest
from tests.fixtures.hardware_device_fixture import create_hardware_device, HARDWARE_DEVICE, hardware_device_repository
from src.resources import exceptions as exc

def test_create_hardware_device(hardware_device_repository, create_hardware_device, actor):
    hardware_device = create_hardware_device(name="Dispositivo de Teste")
    assert hardware_device.id is not None
    assert hardware_device.name == "Dispositivo de Teste"
    assert hardware_device.connection_template_id == 1

def test_update_hardware_device(hardware_device_repository, create_hardware_device, actor):
    hardware_device = create_hardware_device(name="Dispositivo de Teste")
    updated_device = hardware_device_repository.update(hardware_device.id, {"name": "Dispositivo Atualizado"}, actor)
    assert updated_device.name == "Dispositivo Atualizado"

def test_get_hardware_device(hardware_device_repository, create_hardware_device, actor):
    hardware_device = create_hardware_device(name="Dispositivo de Teste")
    fetched_device = hardware_device_repository.get(hardware_device.id, actor)
    assert fetched_device.id == hardware_device.id
    assert fetched_device.name == "Dispositivo de Teste"
