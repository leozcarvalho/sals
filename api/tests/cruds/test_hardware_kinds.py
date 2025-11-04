import pytest
from tests.fixtures.hardware_kind_fixture import create_hardware_kind
from src.cruds.hardware_kind import HardwareKindRepository
from src.domain import exceptions as exc

@pytest.fixture
def hardware_kind_repository(session) -> HardwareKindRepository:
    return HardwareKindRepository(session)

def test_create_hardware_kind(session):
    hw_kind = create_hardware_kind(session, name="Sensor Teste")
    assert hw_kind.id is not None
    assert hw_kind.name == "Sensor Teste"

def test_update_hardware_kind(session, hardware_kind_repository, actor):
    hw_kind = create_hardware_kind(session)
    update_data = {"name": "Sensor Atualizado"}
    updated_hw = hardware_kind_repository.update(hw_kind.id, update_data, actor=actor)
    assert updated_hw.name == "Sensor Atualizado"

def test_delete_hardware_kind(session, hardware_kind_repository):
    hw_kind = create_hardware_kind(session)
    hardware_kind_repository.delete(hw_kind.id)
    
    deleted_hw = hardware_kind_repository.get(hw_kind.id)
    assert deleted_hw is None

def test_get_list_hardware_kinds(session, hardware_kind_repository):
    # cria alguns hardware kinds
    create_hardware_kind(session, name="Sensor 1")
    create_hardware_kind(session, name="Sensor 2")
    create_hardware_kind(session, name="Sensor 3", is_active=False)

    hw_list = hardware_kind_repository.get_list()
    names = [h.name for h in hw_list]

    assert "Sensor 1" in names
    assert "Sensor 2" in names
    assert len(hw_list) >= 2

def test_update_hardware_kind_not_found(hardware_kind_repository, actor):
    with pytest.raises(exc.NotFound):
        hardware_kind_repository.update(9999, {"name": "Não Existe"}, actor=actor)

def test_delete_hardware_kind_not_found(hardware_kind_repository):
    with pytest.raises(exc.NotFound):
        hardware_kind_repository.delete(9999)
