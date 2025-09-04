from fastapi import Depends
from src.routers.base_router import BaseRouter
from src.schemas.room_stall import RoomStall, RoomStallCreate, RoomStallUpdate, RoomStallFilter
from src.cruds.room_stall import RoomStallRepository
from src.core.db import get_session
from src.routers.dependencies import get_current_user


def get_room_stall_service(session = Depends(get_session)):
    return RoomStallRepository(session)

router_room_stalls = BaseRouter(
    prefix="/room-stalls",
    read_schema=RoomStall,
    create_schema=RoomStallCreate,
    update_schema=RoomStallUpdate,
    filter_schema=RoomStallFilter,
    get_service=get_room_stall_service,
    get_current_user=get_current_user,
    tags=["Room Stalls"]
)
