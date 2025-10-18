from .profile import Profile
from .user import User
from .device_pins import DevicePin
from .feeder_valves import FeederValve
from .hardware_connection_template import ConnectionTemplate
from .hardware_device import Device
from .hardware_kind import HardwareKind
from .hardware_point_types import PointType
from .kitchen_tanks import KitchenTank
from .kitchen import Kitchen
from .installations import Installation
from .shed import Shed
from .shed_room import ShedRoom
from .room_stall import RoomStall
from .stall_feeder import StallFeeder
from .healthcheck_priority import HealthcheckPriority
from .product import Product
from .product_tank import ProductTank
from .formula import Formula
from .formula_detail import FormulaDetail
from .feeding_curve import FeedingCurve
from .feeding_curve_detail import FeedingCurveDetail
from .svg import SVG

__all__ = [
    "Profile",
    "User",
    "DevicePin",
    "FeederValve",
    "ConnectionTemplate",
    "Device",
    "HardwareKind",
    "PointType",
    "KitchenTank",
    "Kitchen",
    "Installation",
    "Shed",
    "ShedRoom",
    "RoomStall",
    "StallFeeder",
    "HealthcheckPriority",
    "Product",
    "ProductTank",
    "Formula",
    "FormulaDetail",
    "FeedingCurve",
    "FeedingCurveDetail",
    "SVG",
]

for model_name in __all__:
    globals()[model_name].model_rebuild()
