from fastapi import Depends
from src.cruds.users import UsersRepository
from src.schemas.users import UserBase, UserCreate, UserUpdate, UserRead
from src.routers.base_router import BaseRouter
from src.core.db import get_session

def get_user_service(session = Depends(get_session)):
    return UsersRepository(session)

user_router = BaseRouter(
    prefix="/users",
    tags=["Users"],
    get_service=get_user_service,
    create_schema=UserCreate,
    update_schema=UserUpdate,
    read_schema=UserRead,
    filter_schema=UserBase,
    get_current_user=None
)
