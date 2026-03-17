from fastapi import Depends
from src.routers.base_router import BaseRouter
from src.schemas.feeding_curve import FeedingCurve, FeedingCurveCreate, FeedingCurveUpdate, FeedingCurveFilter
from src.schemas.api_response import ApiResponse
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

@router_feeding_curves.router.post("/clone/{feeding_curve_id}", response_model=ApiResponse)
def clone_feeding_curve(feeding_curve_id: int, feeding_curve_service: FeedingCurveRepository = Depends(get_feeding_curve_service), user=Depends(get_current_user)):
    new_feeding_curve = feeding_curve_service.clone_feeding_curve(feeding_curve_id, actor=user)
    return ApiResponse(success=True, data={"feeding_curve": new_feeding_curve})
