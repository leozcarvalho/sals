from fastapi import Depends
from src.routers.base_router import BaseRouter
from src.schemas.valves import Valve, ValveCreate, ValveUpdate, ValveFilter
from src.cruds.valves import ValveRepository
from src.core.db import get_session
from src.routers.dependencies import get_current_user
from src.domain.permissions import PermissionEnum

def get_valve_service(session = Depends(get_session)):
    return ValveRepository(session)

router_valves = BaseRouter(
    prefix="/valves",
    read_schema=Valve,
    create_schema=ValveCreate,
    update_schema=ValveUpdate,
    filter_schema=ValveFilter,
    get_service=get_valve_service,
    get_current_user=get_current_user,
    tags=["Valves"],
    default_permission=PermissionEnum.MANAGE_VALVE,
)
