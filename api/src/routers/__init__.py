from .auth import auth_router
from .instalations import router_instalations
#from .users import user_router
from .hardware_connection_template import router_hardware_connection_templates
from .hardware_kind import router_hardware_kinds
from .hardware_point_types import router_hardware_point_types
from .hardware_device import router_hardware_devices
from .device_pins import router_device_pins

routers = [
    auth_router,
    router_instalations.router,
    #user_router,
    router_hardware_connection_templates.router,
    router_hardware_kinds.router,
    router_hardware_point_types.router,
    router_hardware_devices.router,
    router_device_pins.router,
]
