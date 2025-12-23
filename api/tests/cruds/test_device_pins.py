import pytest
from src.domain import exceptions as exc
from src.cruds.device_pins import DevicePinRepository
from tests.fixtures.installation_full_fixture import create_installations
from tests.fixtures.product_fixture import create_product
from tests.fixtures.product_tank_fixture import create_product_tank
from tests.fixtures.kitchen_fixture import create_kitchen
from tests.fixtures.shed_fixture import create_shed
from tests.fixtures.sala_fixture import create_sala
from tests.fixtures.baia_fixture import create_baia
from tests.fixtures.comedouro_fixture import create_comedouro
from tests.fixtures.feeder_valve_fixture import create_feeder_valve

def test_get_pins_binary_and_decimal(session, create_installations):
    installation = create_installations
    repo = DevicePinRepository(session)
    pins = repo.get_list(filters={"installation_id": installation.id})
    decimal, binary = repo.get_pins_binary_and_decimal(installation.id)

    assert isinstance(decimal, int)
    assert isinstance(binary, str)
    assert len(binary) == len(pins)
    assert set(binary).issubset({"0", "1"})
    assert decimal == 0  # fresh installation pins are created inactive by default

def test_activate_deactivate_and_toggle_pin(session, create_installations):
    installation = create_installations
    repo = DevicePinRepository(session)
    pins = repo.get_list(filters={"installation_id": installation.id})
    pin = pins[0]

    repo.activate_pin(pin.id)
    p = repo.get(pin.id)
    assert p.is_active is True

    repo.deactivate_pin(pin.id)
    p = repo.get(pin.id)
    assert p.is_active is False

    repo.toggle_pin(pin.id)
    p = repo.get(pin.id)
    assert p.is_active is True

def test_deactivate_all_pins(session, create_installations):
    installation = create_installations
    repo = DevicePinRepository(session)
    pins = repo.get_list(filters={"installation_id": installation.id})

    # activate a couple of pins
    repo.activate_pin(pins[0].id)
    repo.activate_pin(pins[1].id)

    repo.deactivate_all_pins(installation.id)
    pins_after = repo.get_list(filters={"installation_id": installation.id})
    assert all(p.is_active is False for p in pins_after)

def test_get_pin_usage_and_is_valid_pin(session, create_installations):
    installation = create_installations
    repo = DevicePinRepository(session)
    pins = repo.get_list(filters={"installation_id": installation.id})
    # use different pins for different usages
    pin_product = pins[0]
    pin_kitchen = pins[1]
    pin_room = pins[2]
    pin_feeder = pins[3]
    pump_pin = pins[4]
    scale_pin = pins[5]

    # product tank usage
    product = create_product(session, name="Produto Teste")
    product_tank = create_product_tank(session, product_id=product.id, pin_id=pin_product.id, name="PT-1")
    usage = repo.get_pin_usage(pin_product.id)
    assert usage is not None and "tanque de produto" in usage

    with pytest.raises(exc.InvalidData):
        repo._is_valid_pin(pin_product.id)

    # kitchen usage (as shaker/pump/scale)
    kitchen = create_kitchen(session, tanks=[], shaker_pin_id=pin_kitchen.id, pump_pin_id=pump_pin.id, scale_pin_id=scale_pin.id, installation_id=installation.id)
    usage_k = repo.get_pin_usage(pin_kitchen.id)
    assert usage_k is not None and "misturador" in usage_k

    shed = create_shed(session, name="Shed Teste")
    # sala entrance usage
    sala = create_sala(session, shed_id=shed.id, entrance_pin_id=pin_room.id, name="Sala Teste")
    usage_r = repo.get_pin_usage(pin_room.id)
    assert usage_r is not None and "entrada da sala" in usage_r

    # feeder valve usage
    baia = create_baia(session, sala_id=sala.id, name="Baia Teste")
    feeder = create_comedouro(session, baia_id=baia.id, name="Feeder Teste")
    fv = create_feeder_valve(session, device_pin_id=pin_feeder.id, comedouro_id=feeder.id)
    usage_f = repo.get_pin_usage(pin_feeder.id)
    assert usage_f is not None and "válvula" in usage_f

def test_get_grouped_not_used_device_pins(session, create_installations):
    installation = create_installations
    repo = DevicePinRepository(session)
    grouped = repo.get_grouped_not_used_device_pins()

    assert isinstance(grouped, list)
    assert len(grouped) > 0
    first = grouped[0]
    assert "board" in first and "pins" in first
    assert isinstance(first["pins"], list)
    # each pin dict should contain expected keys
    for pin in first["pins"]:
        assert "id" in pin and "name" in pin and "number" in pin and "is_active" in pin and "in_use" in pin