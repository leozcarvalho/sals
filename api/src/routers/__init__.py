from .auth import auth_router
from .profile import router_profiles
from .installations import router_installations
from .users import router_user
from .hardware_connection_template import router_hardware_connection_templates
from .hardware_kind import router_hardware_kinds
from .hardware_point_types import router_hardware_point_types
from .hardware_device import router_hardware_devices
from .device_pins import router_device_pins
from .shed import router_sheds
from .sala import router_salas
from .kitchen import router_kitchens
from .feeder_valves import router_feeder_valves
from .baia import router_baia
from .comedouro import router_comedouros
from .healthcheck_priority import router_healthcheck_priorities
from .product import router_products
from .product_tank import router_product_tanks
from .formula import router_formulas
from .feeding_curve import router_feeding_curves
from .dashboard import router_dashboard
from .svg import router_svgs
from .svg_region import router_svg_region
from .batch import router_batches
from .moviment_kinds import router_moviment_kinds

routers = [
    auth_router,
    router_profiles.router,
    router_installations.router,
    router_user.router,
    router_hardware_connection_templates.router,
    router_hardware_kinds.router,
    router_hardware_point_types.router,
    router_hardware_devices.router,
    router_device_pins.router,
    router_sheds.router,
    router_salas.router,
    router_kitchens.router,
    router_baia.router,
    router_feeder_valves.router,
    router_comedouros.router,
    router_healthcheck_priorities.router,
    router_products.router,
    router_product_tanks.router,
    router_formulas.router,
    router_feeding_curves.router,
    router_dashboard,
    router_svgs.router,
    router_svg_region.router,
    router_batches.router,
    router_moviment_kinds.router,
]
