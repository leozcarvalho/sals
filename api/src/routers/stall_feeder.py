from fastapi import Depends
from src.routers.base_router import BaseRouter
from src.schemas.stall_feeder import StallFeeder, StallFeederCreate, StallFeederUpdate, StallFeederFilter
from src.cruds.stall_feeder import StallFeederRepository
from src.core.db import get_session
from src.routers.dependencies import get_current_user


def get_stall_feeder_service(session = Depends(get_session)):
    return StallFeederRepository(session)

router_stall_feeders = BaseRouter(
    prefix="/stall-feeders",
    read_schema=StallFeeder,
    create_schema=StallFeederCreate,
    update_schema=StallFeederUpdate,
    filter_schema=StallFeederFilter,
    get_service=get_stall_feeder_service,
    get_current_user=get_current_user,
    tags=["Stall Feeders"]
)
