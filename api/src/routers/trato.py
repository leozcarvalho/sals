from typing import List
from fastapi import Depends, Body
from src.routers.base_router import BaseRouter
from src.schemas.trato import TratoCreate, TratoRead, TratoUpdate, TratoFilter, TratoUpdateWithId
from src.schemas.api_response import ApiResponse
from src.cruds.trato import TratoRepository
from src.core.db import get_session
from src.routers.dependencies import get_current_user
from src.domain.permissions import PermissionEnum

def get_trato_service(session = Depends(get_session)):
    return TratoRepository(session)

router_trato = BaseRouter(
    prefix="/tratos",
    read_schema=TratoRead,
    create_schema=TratoCreate,
    update_schema=TratoUpdate,
    filter_schema=TratoFilter,
    get_service=get_trato_service,
    get_current_user=get_current_user,
    tags=["Tratos"],
    default_permission=PermissionEnum.MANAGE_TRATO,
    exclude_routes=["create", "delete", "update"]
)

@router_trato.router.put("/bulk-update", response_model=ApiResponse[List[TratoUpdateWithId]])
def bulk_update_tratos(
    tratos: List[TratoUpdateWithId] = Body(...),
    service: TratoRepository = Depends(get_trato_service),
    current_user = Depends(get_current_user)
):
    service.bulk_update(tratos, actor=current_user)
    return ApiResponse(success=True, data=tratos)
