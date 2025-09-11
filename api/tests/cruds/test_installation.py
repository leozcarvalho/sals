import pytest
from tests.fixtures.installation_fixture import INSTALLATION, create_installation
from tests.fixtures.hardware_connection_template_fixture import create_hardware_connection_template
from tests.fixtures.hardware_device_fixture import create_hardware_device
from tests.fixtures.hardware_kind_fixture import create_hardware_kind
from tests.fixtures.hardware_point_types_fixture import create_hardware_point_type
from src.cruds.installations import InstallationRepository

@pytest.fixture
def installation_repository(session) -> InstallationRepository:
    return InstallationRepository(session)

def test_create_installation(session, installation_repository):
    data = INSTALLATION.model_dump()
    hardware_kind = create_hardware_kind(session)
    hardware_point_type = create_hardware_point_type(session)
    hardware_connection_template = create_hardware_connection_template(session)
    hardware_device = create_hardware_device(session,
                                             hardware_kind_id=hardware_kind.id,
                                             point_type_id=hardware_point_type.id,
                                             connection_template_id=hardware_connection_template.id)

    installation = installation_repository.save(data)
    assert installation.id is not None
    assert installation.device_id == hardware_device.id
    assert installation.device is not None