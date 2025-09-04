from fastapi import Depends
from src.routers.base_router import BaseRouter
from src.schemas.hardware_point_types import HardwarePointType, HardwarePointTypeCreate, HardwarePointTypeUpdate, HardwarePointTypeFilter
from src.cruds.hardware_point_types import HardwarePointTypeRepository
from src.core.db import get_session
from src.routers.dependencies import get_current_user


def get_hardware_point_type_service(session = Depends(get_session)):
    return HardwarePointTypeRepository(session)

router_hardware_point_types = BaseRouter(
    prefix="/hardware-point-types",
    read_schema=HardwarePointType,
    create_schema=HardwarePointTypeCreate,
    update_schema=HardwarePointTypeUpdate,
    filter_schema=HardwarePointTypeFilter,
    get_service=get_hardware_point_type_service,
    get_current_user=get_current_user,
    tags=["Hardware Point Types"]
)
