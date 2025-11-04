import pytest
from tests.fixtures.installation_fixture import create_installation
from tests.fixtures.hardware_connection_template_fixture import create_hardware_connection_template
from tests.fixtures.hardware_device_fixture import create_hardware_device
from tests.fixtures.hardware_kind_fixture import create_hardware_kind
from tests.fixtures.hardware_point_types_fixture import create_hardware_point_type
from tests.fixtures.kitchen_tank_fixture import create_kitchen_tank

@pytest.fixture
def create_installations(session):
    hardware_kind = create_hardware_kind(session)
    hardware_point_type = create_hardware_point_type(session)
    hardware_connection_template = create_hardware_connection_template(session)
    hardware_device = create_hardware_device(session,
                                             hardware_kind_id=hardware_kind.id,
                                             point_type_id=hardware_point_type.id,
                                             connection_template_id=hardware_connection_template.id)
    installation = create_installation(session, device_id=hardware_device.id)
    return installation