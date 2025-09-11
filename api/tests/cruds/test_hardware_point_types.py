import pytest
from tests.fixtures.hardware_point_types_fixture import hardware_point_type_repository, create_hardware_point_type

def test_create_hardware_point_type(create_hardware_point_type):
    hw_point_type = create_hardware_point_type(points_quantity=32, kind="bits")
    assert hw_point_type.id is not None
    assert hw_point_type.points_quantity == 32
    assert hw_point_type.kind == "bits"

def test_update_hardware_point_type(create_hardware_point_type, hardware_point_type_repository, actor):
    hw_point_type = create_hardware_point_type(points_quantity=16, kind="analog")
    update_data = {"points_quantity": 64, "kind": "digital"}
    updated_hw = hardware_point_type_repository.update(hw_point_type.id, update_data, actor=actor)

def test_delete_hardware_point_type(create_hardware_point_type, hardware_point_type_repository):
    hw_point_type = create_hardware_point_type(points_quantity=8, kind="sensor")
    hardware_point_type_repository.delete(hw_point_type.id)
    deleted_hw = hardware_point_type_repository.get(hw_point_type.id)
    assert deleted_hw is None

def test_get_list_hardware_point_types(create_hardware_point_type, hardware_point_type_repository):
    # cria alguns hardware point types
    create_hardware_point_type(points_quantity=16, kind="type1")
    create_hardware_point_type(points_quantity=32, kind="type2")

    hw_list = hardware_point_type_repository.get_list()
    kinds = [h.kind for h in hw_list]

    assert "type1" in kinds
    assert "type2" in kinds
    assert len(hw_list) >= 2
