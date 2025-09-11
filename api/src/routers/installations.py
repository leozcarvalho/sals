from fastapi import Depends
from src.routers.dependencies import get_current_user

from src.core.db import get_session
from src.schemas.installations import Installation, InstallationCreate, InstallationUpdate, InstallationFilter
from src.schemas.api_response import ApiResponse
from src.schemas.users import UserBase
from src.cruds.installations import InstallationRepository
from src.routers.base_router import BaseRouter
from src.domain.permissions import PermissionEnum

def get_installation_service(session=Depends(get_session)):
    return InstallationRepository(session)

router_installations = BaseRouter(
    prefix="/installations",
    read_schema=Installation,
    create_schema=InstallationCreate,
    update_schema=InstallationUpdate,
    filter_schema=InstallationFilter,
    get_service=get_installation_service,
    get_current_user=get_current_user,
    tags=["Instalações"],
    default_permission=PermissionEnum.MANAGE_INSTALLATION,
)

@router_installations.router.post("/{installation_id}/health-check")
def health_check(installation_id: int, service: InstallationRepository = Depends(get_installation_service), current_user: UserBase = Depends(get_current_user)):
    service.health_check(installation_id, current_user)
    return ApiResponse(success=True)

@router_installations.router.post("/{installation_id}/restart")
def restart_device(instalation_id: int, service: InstallationRepository = Depends(get_installation_service), current_user: UserBase = Depends(get_current_user)):
    service.restart_device(instalation_id, current_user)
    return ApiResponse(success=True)

@router_installations.router.post("/{installation_id}/toggle-pin/{pin_number}")
def toggle_pin(installation_id: int, pin_number: int, service: InstallationRepository = Depends(get_installation_service), current_user: UserBase = Depends(get_current_user)):
    service.toggle_pin(installation_id, pin_number, current_user)
    return ApiResponse(success=True)
