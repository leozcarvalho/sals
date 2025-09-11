from fastapi import Depends
from src.routers.base_router import BaseRouter
from src.schemas.hardware_kind import HardwareKindCreate, HardwareKindUpdate, HardwareKind, HardwareKindFilter
from src.cruds.hardware_kind import HardwareKindRepository
from src.core.db import get_session
from src.routers.dependencies import get_current_user
from src.domain.permissions import PermissionEnum

def get_hardware_kind_service(session = Depends(get_session)):
    return HardwareKindRepository(session)

router_hardware_kinds = BaseRouter(
    prefix="/hardware-kinds",
    read_schema=HardwareKind,
    create_schema=HardwareKindCreate,
    update_schema=HardwareKindUpdate,
    filter_schema=HardwareKindFilter,
    get_service=get_hardware_kind_service,
    get_current_user=get_current_user,
    tags=["Hardware Kinds"],
    default_permission=PermissionEnum.MANAGE_HARDWARE_KIND,
)
