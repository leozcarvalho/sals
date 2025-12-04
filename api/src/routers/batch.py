from fastapi import Depends
from src.routers.base_router import BaseRouter
from src.schemas.batch import BatchCreate, BatchUpdate, BatchFilter, Batch
from src.cruds.batch import BatchRepository
from src.core.db import get_session
from src.routers.dependencies import get_current_user
from src.domain.permissions import PermissionEnum

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
