from fastapi import Depends
from src.routers.base_router import BaseRouter
from src.schemas.sala import SalaCreate, SalaUpdate, Sala, SalaFilter
from src.cruds.sala import SalaRepository
from src.core.db import get_session
from src.routers.dependencies import get_current_user
from src.domain.permissions import PermissionEnum


def get_sala_service(session = Depends(get_session)):
    return SalaRepository(session)

router_salas = BaseRouter(
    prefix="/salas",
    read_schema=Sala,
    create_schema=SalaCreate,
    update_schema=SalaUpdate,
    filter_schema=SalaFilter,
    get_service=get_sala_service,
    get_current_user=get_current_user,
    tags=["Salas"],
    default_permission=PermissionEnum.MANAGE_SALA,
)
