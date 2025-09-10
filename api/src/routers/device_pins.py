from fastapi import Depends
from src.routers.base_router import BaseRouter
from src.schemas.device_pins import DevicePin, DevicePinCreate, DevicePinUpdate, DevicePinFilter
from src.cruds.device_pins import DevicePinRepository
from src.core.db import get_session
from src.routers.dependencies import get_current_user
from src.schemas.api_response import ApiResponse

def get_device_pin_service(session = Depends(get_session)):
    return DevicePinRepository(session)

router_device_pins = BaseRouter(
    prefix="/device-pins",
    read_schema=DevicePin,
    create_schema=DevicePinCreate,
    update_schema=DevicePinUpdate,
    filter_schema=DevicePinFilter,
    get_service=get_device_pin_service,
    get_current_user=get_current_user,
    tags=["Device Pins"]
)


@router_device_pins.router.get("/grouped/options")
def get_grouped_not_used_device_pins(
    service: DevicePinRepository = Depends(get_device_pin_service)
):
    return ApiResponse(success=True, data=service.get_grouped_not_used_device_pins(), error=None)