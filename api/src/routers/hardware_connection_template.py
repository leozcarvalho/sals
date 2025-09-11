from fastapi import Depends
from src.routers.base_router import BaseRouter
from src.schemas.hardware_connection_template import HardwareConnectionTemplateCreate, HardwareConnectionTemplateUpdate, HardwareConnectionTemplate, HardwareConnectionTemplateFilter
from src.cruds.hardware_connection_template import HardwareConnectionTemplateRepository
from src.core.db import get_session
from src.routers.dependencies import get_current_user
from src.domain.permissions import PermissionEnum

def get_hardware_connection_template_service(session = Depends(get_session)):
    return HardwareConnectionTemplateRepository(session)

router_hardware_connection_templates = BaseRouter(
    prefix="/hardware-connection-templates",
    read_schema=HardwareConnectionTemplate,
    create_schema=HardwareConnectionTemplateCreate,
    update_schema=HardwareConnectionTemplateUpdate,
    filter_schema=HardwareConnectionTemplateFilter,
    get_service=get_hardware_connection_template_service,
    get_current_user=get_current_user,
    tags=["Hardware Connection Templates"],
    default_permission=PermissionEnum.MANAGE_HARDWARE_CONNECTION_TEMPLATE,
)
