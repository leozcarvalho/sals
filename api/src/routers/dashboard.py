from fastapi import Depends
from fastapi import APIRouter

from src.schemas.users import UserBase
from src.schemas.api_response import ApiResponse
from src.cruds.dashboard import DashboardRepository
from src.core.db import get_session
from src.routers.dependencies import get_current_user

router_dashboard = APIRouter(prefix="/dashboard", tags=["Dashboard"])

def get_dashboard_repository(session = Depends(get_session)):
    return DashboardRepository(session)

@router_dashboard.get("/svg-data")
def get_data_svg(current_user: UserBase = Depends(get_current_user), repo: DashboardRepository = Depends(get_dashboard_repository)):
    data = repo.get_data_from_svg()
    return ApiResponse(success=True, data=data, error=None)
