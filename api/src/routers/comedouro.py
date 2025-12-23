from fastapi import Depends
from src.routers.base_router import BaseRouter
from src.schemas.comedouro import Comedouro, ComedouroCreate, ComedouroUpdate, ComedouroFilter
from src.cruds.comedouro import ComedouroRepository
from src.core.db import get_session
from src.routers.dependencies import get_current_user
from src.domain.permissions import PermissionEnum

def get_comedouro_service(session = Depends(get_session)):
    return ComedouroRepository(session)

router_comedouros = BaseRouter(
    prefix="/comedouros",
    read_schema=Comedouro,
    create_schema=ComedouroCreate,
    update_schema=ComedouroUpdate,
    filter_schema=ComedouroFilter,
    get_service=get_comedouro_service,
    get_current_user=get_current_user,
    tags=["Comedouros"],
    default_permission=PermissionEnum.MANAGE_COMEDOURO,
)
