from fastapi import Depends
from src.routers.base_router import BaseRouter
from src.schemas.baia import Baia, BaiaCreate, BaiaUpdate, BaiaFilter
from src.cruds.baia import BaiaRepository
from src.core.db import get_session
from src.routers.dependencies import get_current_user
from src.domain.permissions import PermissionEnum

def get_baia_service(session = Depends(get_session)):
    return BaiaRepository(session)

router_baia = BaseRouter(
    prefix="/baias",
    read_schema=Baia,
    create_schema=BaiaCreate,
    update_schema=BaiaUpdate,
    filter_schema=BaiaFilter,
    get_service=get_baia_service,
    get_current_user=get_current_user,
    tags=["Baias"],
    default_permission=PermissionEnum.MANAGE_BAIA,
)
