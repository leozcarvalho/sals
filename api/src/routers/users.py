from fastapi import Depends
from src.cruds.users import UsersRepository
from src.schemas.users import UserBase, UserCreate, UserUpdate, UserRead, UserFilter
from src.routers.base_router import BaseRouter
from src.core.db import get_session
from src.routers.dependencies import get_current_user
from src.schemas.api_response import ApiResponse

def get_user_service(session = Depends(get_session)):
    return UsersRepository(session)

router_user = BaseRouter(
    prefix="/users",
    create_schema=UserCreate,
    update_schema=UserUpdate,
    read_schema=UserRead,
    filter_schema=UserFilter,
    get_service=get_user_service,
    get_current_user=get_current_user,
    tags=["Users"]
)


@router_user.router.get("/current/self")
def list_me(current_user: UserBase = Depends(get_current_user)):
    return ApiResponse(success=True, data=current_user, error=None)