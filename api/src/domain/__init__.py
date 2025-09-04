from .profile import Profile
from .user import User
from .device_pins import DevicePin
from .feeder_valves import FeederValve
from .hardware_connection_template import ConnectionTemplate
from .hardware_device import Device
from .hardware_kind import HardwareKind
from .hardware_point_types import PointType
from .kitchen import Kitchen
from .instalations import Instalation
from .shed import Shed
from .shed_room import ShedRoom
from .room_stall import RoomStall
from .stall_feeder import StallFeeder

__all__ = [
    "Profile",
    "User",
    "DevicePin",
    "FeederValve",
    "ConnectionTemplate",
    "Device",
    "HardwareKind",
    "PointType",
    "Kitchen",
    "Instalation",
    "Shed",
    "ShedRoom",
    "RoomStall",
    "StallFeeder",
]

for model_name in __all__:
    globals()[model_name].update_forward_refs()
