from fastapi import Depends
from src.routers.base_router import BaseRouter
from src.schemas.moviment_kinds import MovimentKind, MovimentKindCreate, MovimentKindUpdate, MovimentKindFilter
from src.cruds.moviment_kinds import MovimentKindRepository
from src.core.db import get_session
from src.routers.dependencies import get_current_user
from src.domain.permissions import PermissionEnum

def get_moviment_kind_service(session = Depends(get_session)):
    return MovimentKindRepository(session)

router_moviment_kinds = BaseRouter(
    prefix="/moviment-kinds",
    read_schema=MovimentKind,
    create_schema=MovimentKindCreate,
    update_schema=MovimentKindUpdate,
    filter_schema=MovimentKindFilter,
    get_service=get_moviment_kind_service,
    get_current_user=get_current_user,
    tags=["Moviment Kinds"],
    default_permission=PermissionEnum.MANAGE_MOVIMENT_KIND,
)
