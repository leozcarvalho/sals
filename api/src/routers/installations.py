from fastapi import Depends, Body
from src.routers.dependencies import get_current_user
from typing import List

from src.core.db import get_session
from src.schemas.installations import Installation, InstallationCreate, InstallationUpdate, InstallationFilter
from src.schemas.device_pins import DevicePinBulkUpdate
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

@router_installations.router.post("/{installation_id}/action/{action}")
def exec_installation_action(
    installation_id: int,
    action: str,
    payload: dict = Body(default={}),
    service: InstallationRepository = Depends(get_installation_service),
    current_user: UserBase = Depends(get_current_user),
):
    """
    Executa uma ação genérica em uma instalação.
    Exemplo de uso:
      POST /installations/1/action/healthcheck
      POST /installations/1/action/restart
      POST /installations/1/action/tare
      POST /installations/1/action/calibrate { "weight": 10.0 }
      POST /installations/1/action/send_value { "value": "0101" }
    """
    result = service.exec_action(installation_id, action, current_user, **payload)
    return result


@router_installations.router.put("/{installation_id}/update-device-pins")
def update_device_pins(
    installation_id: int,
    device_pins: List[DevicePinBulkUpdate],
    service: InstallationRepository = Depends(get_installation_service),
    current_user: UserBase = Depends(get_current_user),
):
    """
    Atualiza os pinos de dispositivo de uma instalação.
    """
    result = service.update_device_pins(installation_id, device_pins, current_user)
    return ApiResponse(success=True, data=result, error=None)
