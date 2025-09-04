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

router_instalations = BaseRouter(
    prefix="/instalations",
    read_schema=Instalation,
    create_schema=InstalationCreate,
    update_schema=InstalationUpdate,
    filter_schema=InstalationFilter,
    get_service=get_instalation_service,
    get_current_user=get_current_user,
    tags=["Instalações"]
)

@router_instalations.router.post("/{instalation_id}/health-check")
def health_check(instalation_id: int, service: InstalationRepository = Depends(get_instalation_service), current_user: UserBase = Depends(get_current_user)):
    service.health_check(instalation_id, current_user)
    return ApiResponse(success=True)

@router_instalations.router.post("/{instalation_id}/restart")
def restart_device(instalation_id: int, service: InstalationRepository = Depends(get_instalation_service), current_user: UserBase = Depends(get_current_user)):
    service.restart_device(instalation_id, current_user)
    return ApiResponse(success=True)

@router_instalations.router.post("/{instalation_id}/toggle-pin/{pin_number}")
def toggle_pin(instalation_id: int, pin_number: int, service: InstalationRepository = Depends(get_instalation_service), current_user: UserBase = Depends(get_current_user)):
    service.toggle_pin(instalation_id, pin_number, current_user)
    return ApiResponse(success=True)
