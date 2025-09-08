from fastapi import Depends
from src.routers.dependencies import get_current_user

from src.core.db import get_session
from src.schemas.instalations import Instalation, InstalationCreate, InstalationUpdate, InstalationFilter
from src.schemas.api_response import ApiResponse
from src.schemas.users import UserBase
from src.cruds.instalations import InstalationRepository
from src.routers.base_router import BaseRouter

def get_instalation_service(session=Depends(get_session)):
    return InstalationRepository(session)

router_installations = BaseRouter(
    prefix="/installations",
    read_schema=Instalation,
    create_schema=InstalationCreate,
    update_schema=InstalationUpdate,
    filter_schema=InstalationFilter,
    get_service=get_instalation_service,
    get_current_user=get_current_user,
    tags=["Instalações"]
)

@router_installations.router.post("/{installation_id}/health-check")
def health_check(installation_id: int, service: InstalationRepository = Depends(get_instalation_service), current_user: UserBase = Depends(get_current_user)):
    service.health_check(installation_id, current_user)
    return ApiResponse(success=True)

@router_installations.router.post("/{installation_id}/restart")
def restart_device(instalation_id: int, service: InstalationRepository = Depends(get_instalation_service), current_user: UserBase = Depends(get_current_user)):
    service.restart_device(instalation_id, current_user)
    return ApiResponse(success=True)

@router_installations.router.post("/{installation_id}/toggle-pin/{pin_number}")
def toggle_pin(installation_id: int, pin_number: int, service: InstalationRepository = Depends(get_instalation_service), current_user: UserBase = Depends(get_current_user)):
    service.toggle_pin(installation_id, pin_number, current_user)
    return ApiResponse(success=True)
