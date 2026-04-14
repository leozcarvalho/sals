from fastapi import Depends
from src.routers.base_router import BaseRouter
from src.schemas.dosador_seco import DosadorSeco, DosadorSecoCreate, DosadorSecoUpdate, DosadorSecoFilter
from src.cruds.dosador_seco import DosadorSecoRepository
from src.core.db import get_session
from src.routers.dependencies import get_current_user
from src.domain.permissions import PermissionEnum

def get_dosador_seco_service(session = Depends(get_session)):
    return DosadorSecoRepository(session)

router_dosador_seco = BaseRouter(
    prefix="/dosadores-secos",
    read_schema=DosadorSeco,
    create_schema=DosadorSecoCreate,
    update_schema=DosadorSecoUpdate,
    filter_schema=DosadorSecoFilter,
    get_service=get_dosador_seco_service,
    get_current_user=get_current_user,
    tags=["Dosador Seco"],
    default_permission=PermissionEnum.MANAGE_DOSADOR_SECO,
)
