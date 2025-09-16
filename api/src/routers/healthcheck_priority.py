from fastapi import Depends
from src.routers.base_router import BaseRouter
from src.schemas.healthcheck_priority import HealthcheckPriority, HealthcheckPriorityCreate, HealthcheckPriorityUpdate, HealthcheckPriorityFilter
from src.cruds.healthcheck_priority import HealthcheckPriorityRepository
from src.core.db import get_session
from src.routers.dependencies import get_current_user
from src.domain.permissions import PermissionEnum

def get_healthcheck_priority_service(session = Depends(get_session)):
    return HealthcheckPriorityRepository(session)

router_healthcheck_priorities = BaseRouter(
    prefix="/healthcheck-priorities",
    read_schema=HealthcheckPriority,
    create_schema=HealthcheckPriorityCreate,
    update_schema=HealthcheckPriorityUpdate,
    filter_schema=HealthcheckPriorityFilter,
    get_service=get_healthcheck_priority_service,
    get_current_user=get_current_user,
    tags=["Healthcheck Priorities"],
    default_permission=PermissionEnum.MANAGE_HEALTHCHECK_PRIORITY,
)
