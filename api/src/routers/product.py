from fastapi import Depends
from src.routers.base_router import BaseRouter
from src.schemas.product import ProductRead, ProductCreate, ProductUpdate, ProductFilter
from src.cruds.product import ProductRepository
from src.core.db import get_session
from src.routers.dependencies import get_current_user
from src.domain.permissions import PermissionEnum

def get_product_service(session = Depends(get_session)):
    return ProductRepository(session)

router_products = BaseRouter(
    prefix="/products",
    read_schema=ProductRead,
    create_schema=ProductCreate,
    update_schema=ProductUpdate,
    filter_schema=ProductFilter,
    get_service=get_product_service,
    get_current_user=get_current_user,
    tags=["Products"],
    default_permission=PermissionEnum.MANAGE_PRODUCT,
)