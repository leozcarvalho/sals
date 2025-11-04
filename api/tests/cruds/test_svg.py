import pytest
from src.domain import exceptions as exc
from tests.fixtures.svg_fixture import create_svg, SVG
from tests.fixtures.shed_fixture import create_shed
from tests.fixtures.shed_room_fixture import create_shed_room
from tests.fixtures.room_stall_fixture import create_room_stall
from tests.fixtures.installation_full_fixture import create_installations
from tests.fixtures.product_fixture import create_product
from tests.fixtures.product_tank_fixture import create_product_tank
from tests.fixtures.kitchen_fixture import create_kitchen


from src.cruds.svg import SvgRepository

@pytest.fixture
def svg_repository(session) -> SvgRepository:
    return SvgRepository(session)


def test_get_shed_variables(svg_repository, session):
    shed = create_shed(session)
    shed_room = create_shed_room(session, shed_id=shed.id)
    create_room_stall(session, room_id=shed_room.id)
    svg = create_svg(session, owner_type="sheds", owner_id=shed.id, content="""<svg>{{VAL}}</svg>""")
    variables = svg_repository.get_variables(svg.id)
    assert len(variables) == 2

def test_get_kitchen_variables(svg_repository, session, create_installations):
    product = create_product(session, name="Produto Teste")
    product_tank = create_product_tank(session, product_id=product.id, name="Tanque Teste", pin_id=5)
    kitchen = create_kitchen(session, tanks=[{"product_tank_id": product_tank.id}], shaker_pin_id=10, pump_pin_id=11, scale_pin_id=12, installation_id=create_installations.id)
    svg = create_svg(session, owner_type="kitchens", owner_id=kitchen.id, content="""<svg>{{VAL}}</svg>""")
    variables = svg_repository.get_variables(svg.id)
    assert len(variables) == 2

def test_get_kitchen_options(svg_repository, session, create_installations):
    product = create_product(session, name="Produto Teste")
    product_tank = create_product_tank(session, product_id=product.id, name="Tanque Teste", pin_id=5)
    kitchen = create_kitchen(session, tanks=[{"product_tank_id": product_tank.id}], shaker_pin_id=10, pump_pin_id=11, scale_pin_id=12, installation_id=create_installations.id)
    svg = create_svg(session, owner_type="kitchens", owner_id=kitchen.id, content="""<svg>{{VAL}}</svg>""")
    options = svg_repository.get_options(svg.id)
    assert len(options) == 4

def test_get_installation_variables(svg_repository, session, create_installations):
    installation = create_installations
    svg = create_svg(session, owner_type="installations", owner_id=installation.id, content="""<svg>{{VAL}}</svg>""")
    variables = svg_repository.get_variables(svg.id)
    assert len(variables) == 1

def test_get_installation_options(svg_repository, session, create_installations):
    installation = create_installations
    svg = create_svg(session, owner_type="installations", owner_id=installation.id, content="""<svg>{{VAL}}</svg>""")
    variables = svg_repository.get_options(svg.id)
    assert len(variables) == 32

'''
def test_get_list_svg(svg_repository, session, create_installations):
    installation = create_installations
    svg1 = create_svg(session, owner_type="installations", owner_id=installation.id, name="SVG 1")
    svg2 = create_svg(session, owner_type="installations", owner_id=installation.id, name="SVG 2")
    svg_list = svg_repository.get_list()
'''

def test_svg_with_variables(svg_repository, session, create_installations):
    installation = create_installations
    svg = create_svg(session, owner_type="installations", owner_id=installation.id, content="""<svg>IP</svg>""")
    svg = svg_repository.svg_with_variables(svg.id, replace_variables=True)
    assert svg.content == """<svg>192.168.0.1</svg>"""
