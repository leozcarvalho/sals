from fastapi import Depends
from src.routers.base_router import BaseRouter
from src.schemas.shed import Shed, ShedCreate, ShedUpdate, ShedFilter, ShedCloneRequest
from src.schemas.api_response import ApiResponse
from src.cruds.shed import ShedRepository
from src.core.db import get_session
from src.routers.dependencies import get_current_user
from src.domain.permissions import PermissionEnum

def get_shed_service(session = Depends(get_session)):
    return ShedRepository(session)

router_sheds = BaseRouter(
    prefix="/sheds",
    read_schema=Shed,
    create_schema=ShedCreate,
    update_schema=ShedUpdate,
    filter_schema=ShedFilter,
    get_service=get_shed_service,
    get_current_user=get_current_user,
    tags=["Sheds"],
    default_permission=PermissionEnum.MANAGE_SHED,
)

@router_sheds.router.post("/clone/{shed_id}", response_model=ApiResponse)
def clone_shed(shed_id: int, shed_service: ShedRepository = Depends(get_shed_service), user=Depends(get_current_user)):
    new_shed = shed_service.clone_shed(shed_id, actor=user)
    return ApiResponse(success=True, data={"shed": new_shed})
