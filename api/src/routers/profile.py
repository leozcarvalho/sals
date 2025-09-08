from fastapi import Depends
from src.routers.base_router import BaseRouter
from src.schemas.profile import ProfileRead, ProfileCreate, ProfileUpdate, ProfileFilter
from src.schemas.api_response import ApiResponse
from src.cruds.profile import ProfileRepository
from src.core.db import get_session
from src.routers.dependencies import get_current_user

def get_profile_service(session = Depends(get_session)):
    return ProfileRepository(session)

router_profiles = BaseRouter(
    prefix="/profiles",
    read_schema=ProfileRead,
    create_schema=ProfileCreate,
    update_schema=ProfileUpdate,
    filter_schema=ProfileFilter,
    get_service=get_profile_service,
    get_current_user=get_current_user,
    tags=["Profiles"]
)

@router_profiles.router.get("/permissions/all", summary="List all available permissions")
def list_permissions(service: ProfileRepository = Depends(get_profile_service), current_user = Depends(get_current_user)):
    permissions = service.get_permissions()
    return ApiResponse(success=True, error=None, data=permissions)
