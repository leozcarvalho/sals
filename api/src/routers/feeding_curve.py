from fastapi import Depends
from src.routers.base_router import BaseRouter
from src.schemas.feeding_curve import FeedingCurve, FeedingCurveCreate, FeedingCurveUpdate, FeedingCurveFilter
from src.cruds.feeding_curve import FeedingCurveRepository
from src.core.db import get_session
from src.routers.dependencies import get_current_user
from src.domain.permissions import PermissionEnum

def get_feeding_curve_service(session = Depends(get_session)):
    return FeedingCurveRepository(session)

router_feeding_curves = BaseRouter(
    prefix="/feeding-curves",
    read_schema=FeedingCurve,
    create_schema=FeedingCurveCreate,
    update_schema=FeedingCurveUpdate,
    filter_schema=FeedingCurveFilter,
    get_service=get_feeding_curve_service,
    get_current_user=get_current_user,
    tags=["Feeding Curves"],
    default_permission=PermissionEnum.MANAGE_FEEDING_CURVE,
)