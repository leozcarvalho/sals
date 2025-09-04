from .auth import auth_router
from .profile import router_profiles
from .instalations import router_instalations
from .users import router_user
from .hardware_connection_template import router_hardware_connection_templates
from .hardware_kind import router_hardware_kinds
from .hardware_point_types import router_hardware_point_types
from .hardware_device import router_hardware_devices
from .device_pins import router_device_pins
from .shed import router_sheds
from .shed_room import router_shed_rooms
from .kitchen import router_kitchens
from .feeder_valves import router_feeder_valves
from .stall_feeder import router_stall_feeders

routers = [
    auth_router,
    router_profiles.router,
    router_instalations.router,
    router_user.router,
    router_hardware_connection_templates.router,
    router_hardware_kinds.router,
    router_hardware_point_types.router,
    router_hardware_devices.router,
    router_device_pins.router,
    router_sheds.router,
    router_shed_rooms.router,
    router_kitchens.router,
    router_feeder_valves.router,
    router_stall_feeders.router,
]
