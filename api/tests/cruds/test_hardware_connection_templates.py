import pytest
from tests.fixtures.hardware_connection_template_fixture import create_hardware_connection_template, HARDWARE_CONNECTION_TEMPLATE
from src.cruds.hardware_connection_template import HardwareConnectionTemplateRepository

@pytest.fixture
def hardware_connection_template_repository(session) -> HardwareConnectionTemplateRepository:
    return HardwareConnectionTemplateRepository(session)

def test_create_hardware_connection_template(hardware_connection_template_repository, actor):
    hw_template = HARDWARE_CONNECTION_TEMPLATE.model_copy()
    created_template = hardware_connection_template_repository.save(hw_template.model_dump(), actor=actor)
    assert created_template.id is not None
    assert created_template.name == hw_template.name

def test_update_hardware_connection_template(session, hardware_connection_template_repository, actor):
    hw_template = create_hardware_connection_template(session, name="Template Inicial", template_url="http://template_inicial.com")
    update_data = {"name": "Template Atualizado"}
    updated_template = hardware_connection_template_repository.update(hw_template.id, update_data, actor=actor)
    assert updated_template.name == "Template Atualizado"

def test_delete_hardware_connection_template(session, hardware_connection_template_repository):
    hw_template = create_hardware_connection_template(session, name="Template Deletar", template_url="http://template_deletar.com")
    hardware_connection_template_repository.delete(hw_template.id)
    deleted_template = hardware_connection_template_repository.get(hw_template.id)
    assert deleted_template is None

def test_get_list_hardware_connection_templates(session, hardware_connection_template_repository):
    create_hardware_connection_template(session, name="Template 1", template_url="http://template1.com")
    create_hardware_connection_template(session, name="Template 2", template_url="http://template2.com", is_active=False)
    hw_list = hardware_connection_template_repository.get_list()
    names = [h.name for h in hw_list]
    assert "Template 1" in names
    assert "Template 2" in names
    assert len(hw_list) >= 2
