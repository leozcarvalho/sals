from fastapi import Depends
from src.routers.base_router import BaseRouter
from src.schemas.hardware_device import HardwareDeviceCreate, HardwareDeviceUpdate, HardwareDevice, HardwareDeviceFilter
from src.cruds.hardware_device import HardwareDeviceRepository
from src.core.db import get_session
from src.routers.dependencies import get_current_user


def get_hardware_device_service(session = Depends(get_session)):
    return HardwareDeviceRepository(session)

router_hardware_devices = BaseRouter(
    prefix="/hardware-devices",
    read_schema=HardwareDevice,
    create_schema=HardwareDeviceCreate,
    update_schema=HardwareDeviceUpdate,
    filter_schema=HardwareDeviceFilter,
    get_service=get_hardware_device_service,
    get_current_user=get_current_user,
    tags=["Hardware Devices"]
)
