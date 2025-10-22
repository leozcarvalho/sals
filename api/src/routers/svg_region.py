from fastapi import Depends
from src.routers.base_router import BaseRouter
from src.schemas.svg_region import SVGRegionRead, SVGRegionCreate, SVGRegionUpdate, SVGRegionFilter
from src.cruds.svg_region import SvgRegionRepository
from src.core.db import get_session
from src.routers.dependencies import get_current_user
from src.domain.permissions import PermissionEnum

def get_svg_region_service(session = Depends(get_session)):
    return SvgRegionRepository(session)

router_svg_region = BaseRouter(
    prefix="/svg-regions",
    read_schema=SVGRegionRead,
    create_schema=SVGRegionCreate,
    update_schema=SVGRegionUpdate,
    filter_schema=SVGRegionFilter,
    get_service=get_svg_region_service,
    get_current_user=get_current_user,
    tags=["SVG Regions"],
    default_permission=PermissionEnum.MANAGE_SVG,
)
