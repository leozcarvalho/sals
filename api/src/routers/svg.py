from fastapi import Depends
from typing import Optional
from src.routers.base_router import BaseRouter
from src.schemas.svg import SVGRead, SVGCreate, SVGUpdate, SVGFilter
from src.schemas.api_response import ApiResponse
from src.cruds.svg import SvgRepository
from src.core.db import get_session
from src.routers.dependencies import get_current_user
from src.domain.permissions import PermissionEnum

def get_svg_service(session = Depends(get_session)):
    return SvgRepository(session)

router_svgs = BaseRouter(
    prefix="/svgs",
    read_schema=SVGRead,
    create_schema=SVGCreate,
    update_schema=SVGUpdate,
    filter_schema=SVGFilter,
    get_service=get_svg_service,
    get_current_user=get_current_user,
    tags=["SVGs"],
    default_permission=PermissionEnum.MANAGE_SVG,
    exclude_routes=["get"]
)

@router_svgs.router.get("/{svg_id}", response_model=ApiResponse)
def get_svg_by_id(svg_id: int, replace_variables: Optional[bool] = None, service: SvgRepository = Depends(get_svg_service), current_user = Depends(get_current_user)):
    router_svgs._check_permission(current_user, "read")
    svg = service.svg_with_variables(svg_id, replace_variables=replace_variables)
    return ApiResponse(success=True, data=svg, error=None)

@router_svgs.router.get("/{svg_id}/options")
def get_svg_options(svg_id: int, service: SvgRepository = Depends(get_svg_service), current_user = Depends(get_current_user)):
    router_svgs._check_permission(current_user, "read")
    data = service.get_options(svg_id)
    return ApiResponse(success=True, data=data, error=None)

@router_svgs.router.get("/{svg_id}/variables")
def get_svg_variables(svg_id: int, service: SvgRepository = Depends(get_svg_service), current_user = Depends(get_current_user)):
    router_svgs._check_permission(current_user, "read")
    variables = service.get_variables(svg_id)
    return ApiResponse(success=True, data=variables, error=None)

@router_svgs.router.get("/owner/{owner_type}/{owner_id}")
def get_svg_by_owner(owner_type: str, owner_id: int, service: SvgRepository = Depends(get_svg_service), current_user = Depends(get_current_user)):
    router_svgs._check_permission(current_user, "read")
    svg_id = service.get_owner_svg_id(owner_type, owner_id)
    return ApiResponse(success=True, data={"svg_id": svg_id}, error=None)
