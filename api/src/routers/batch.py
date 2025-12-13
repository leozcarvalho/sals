from fastapi import Depends, Body
from src.routers.base_router import BaseRouter
from src.schemas.batch import BatchCreate, BatchUpdate, BatchFilter, Batch
from src.cruds.batch import BatchRepository
from src.core.db import get_session
from src.routers.dependencies import get_current_user
from src.domain.permissions import PermissionEnum
from src.schemas.users import UserBase
from src.schemas.api_response import ApiResponse
from src.schemas.moviment import MovimentBase

def get_batch_service(session = Depends(get_session)):
    return BatchRepository(session)

router_batches = BaseRouter(
    prefix="/batches",
    read_schema=Batch,
    create_schema=BatchCreate,
    update_schema=BatchUpdate,
    filter_schema=BatchFilter,
    get_service=get_batch_service,
    get_current_user=get_current_user,
    tags=["Batches"],
    default_permission=PermissionEnum.MANAGE_BATCH,
)

@router_batches.router.post("/{batch_id}/moviment")
def exec_batch_moviment_action(
    batch_id: int,
    moviment: MovimentBase = Body(...),
    batch_service: BatchRepository = Depends(get_batch_service),
    current_user: UserBase = Depends(get_current_user),
):
    data = batch_service.exec_batch_moviment(batch_id, moviment.model_dump(), actor=current_user)
    return ApiResponse(success=True, data=data, error=None)
