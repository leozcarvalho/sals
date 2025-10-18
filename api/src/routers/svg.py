from fastapi import Depends
from src.routers.base_router import BaseRouter
from src.schemas.svg import SVGRead, SVGCreate, SVGUpdate, SVGFilter
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
)
