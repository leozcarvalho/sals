from fastapi import Depends
from src.routers.base_router import BaseRouter
from src.schemas.kicthen import Kitchen, KitchenCreate, KitchenUpdate, KitchenFilter
from src.cruds.kitchen import KitchenRepository
from src.core.db import get_session
from src.routers.dependencies import get_current_user
from src.domain.permissions import PermissionEnum

def get_kitchen_service(session = Depends(get_session)):
    return KitchenRepository(session)

router_kitchens = BaseRouter(
    prefix="/kitchens",
    read_schema=Kitchen,
    create_schema=KitchenCreate,
    update_schema=KitchenUpdate,
    filter_schema=KitchenFilter,
    get_service=get_kitchen_service,
    get_current_user=get_current_user,
    tags=["Kitchens"],
    default_permission=PermissionEnum.MANAGE_KITCHEN,
)
