from fastapi import Depends
from src.routers.base_router import BaseRouter
from src.schemas.product_tank import ProductTankRead, ProductTankCreate, ProductTankUpdate, ProductTankFilter
from src.cruds.product_tank import ProductTankRepository
from src.core.db import get_session
from src.routers.dependencies import get_current_user
from src.domain.permissions import PermissionEnum

def get_product_tank_service(session = Depends(get_session)):
    return ProductTankRepository(session)

router_product_tanks = BaseRouter(
    prefix="/product-tanks",
    read_schema=ProductTankRead,
    create_schema=ProductTankCreate,
    update_schema=ProductTankUpdate,
    filter_schema=ProductTankFilter,
    get_service=get_product_tank_service,
    get_current_user=get_current_user,
    tags=["Product Tanks"],
    default_permission=PermissionEnum.MANAGE_PRODUCT_TANK,
)