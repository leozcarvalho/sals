import pytest
from tests.fixtures.kitchen_fixture import create_kitchen, KITCHEN
from tests.fixtures.installation_fixture import create_installation
from tests.fixtures.hardware_connection_template_fixture import create_hardware_connection_template
from tests.fixtures.hardware_device_fixture import create_hardware_device
from tests.fixtures.hardware_kind_fixture import create_hardware_kind
from tests.fixtures.hardware_point_types_fixture import create_hardware_point_type
from tests.fixtures.kitchen_tank_fixture import create_kitchen_tank
from tests.fixtures.product_fixture import create_product
from tests.fixtures.product_tank_fixture import create_product_tank
from src.cruds.kitchen import KitchenRepository
from src.domain import exceptions as exc

@pytest.fixture
def kitchen_repository(session) -> KitchenRepository:
    return KitchenRepository(session)

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


def test_create_kitchen(session, kitchen_repository, create_installations):
    installation = create_installations
    product = create_product(session, name="Produto Teste")
    product_tank = create_product_tank(session, product_id=product.id, name="Tanque Teste", pin_id=5)
    data = KITCHEN.model_dump().copy()
    data['tanks'] = [{"product_tank_id": product_tank.id}]
    kitchen = kitchen_repository.save({**data, "installation_id": installation.id})
    assert kitchen.id is not None
    assert kitchen.name == "Test Kitchen"
    assert len(kitchen.tanks) == 1
    assert kitchen.tanks[0].id == product_tank.id

def test_update_kitchen(session, kitchen_repository, create_installations):
    installation = create_installations
    kitchen = create_kitchen(session, installation_id=installation.id)
    updated_kitchen = kitchen_repository.update(kitchen.id, {"name": "Updated Kitchen"})
    assert updated_kitchen.name == "Updated Kitchen"

def test_used_same_pin(session, kitchen_repository, create_installations):
    installation = create_installations
    kitchen = create_kitchen(session, installation_id=installation.id)
    with pytest.raises(exc.InvalidData) as exc_info:
        kitchen_repository.update(kitchen.id, {
            "shaker_pin_id": 1,
            "pump_pin_id": 1,
            "scale_pin_id": 2
        })
    assert str(exc_info.value) == "Não é permitido usar o mesmo pino em mais de uma função."
