from fastapi import Depends
from src.routers.base_router import BaseRouter
from src.schemas.shed_room import ShedRoom, ShedRoomCreate, ShedRoomUpdate, ShedRoomFilter
from src.cruds.shed_room import ShedRoomRepository
from src.core.db import get_session
from src.routers.dependencies import get_current_user
from src.domain.permissions import PermissionEnum


def get_shed_room_service(session = Depends(get_session)):
    return ShedRoomRepository(session)

router_shed_rooms = BaseRouter(
    prefix="/shed-rooms",
    read_schema=ShedRoom,
    create_schema=ShedRoomCreate,
    update_schema=ShedRoomUpdate,
    filter_schema=ShedRoomFilter,
    get_service=get_shed_room_service,
    get_current_user=get_current_user,
    tags=["Shed Rooms"],
    default_permission=PermissionEnum.MANAGE_SHED_ROOM,
)
