import pytest
from tests.fixtures.hardware_point_types_fixture import create_hardware_point_type
from src.cruds.hardware_point_types import HardwarePointTypeRepository

@pytest.fixture
def hardware_point_type_repository(session) -> HardwarePointTypeRepository:
    return HardwarePointTypeRepository(session)

def test_create_hardware_point_type(session):
    hw_point_type = create_hardware_point_type(session)
    assert hw_point_type.id is not None
    assert hw_point_type.points_quantity == 32
    assert hw_point_type.kind == "bit"

def test_update_hardware_point_type(session, actor, hardware_point_type_repository):
    hw_point_type = create_hardware_point_type(session)
    update_data = {"points_quantity": 64, "kind": "digital"}
    updated_hw = hardware_point_type_repository.update(hw_point_type.id, update_data, actor=actor)

def test_delete_hardware_point_type(session, hardware_point_type_repository):
    hw_point_type = create_hardware_point_type(session)
    hardware_point_type_repository.delete(hw_point_type.id)
    deleted_hw = hardware_point_type_repository.get(hw_point_type.id)
    assert deleted_hw is None

def test_get_list_hardware_point_types(session, hardware_point_type_repository):
    create_hardware_point_type(session, points_quantity=16, kind="type1")
    create_hardware_point_type(session, points_quantity=32, kind="type2")
    hw_list = hardware_point_type_repository.get_list()
    kinds = [h.kind for h in hw_list]
    assert "type1" in kinds
    assert "type2" in kinds
    assert len(hw_list) >= 2
