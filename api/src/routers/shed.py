from fastapi import Depends
from src.routers.base_router import BaseRouter
from src.schemas.shed import Shed, ShedCreate, ShedUpdate, ShedFilter
from src.cruds.shed import ShedRepository
from src.core.db import get_session
from src.routers.dependencies import get_current_user


def get_shed_service(session = Depends(get_session)):
    return ShedRepository(session)

router_sheds = BaseRouter(
    prefix="/sheds",
    read_schema=Shed,
    create_schema=ShedCreate,
    update_schema=ShedUpdate,
    filter_schema=ShedFilter,
    get_service=get_shed_service,
    get_current_user=get_current_user,
    tags=["Sheds"]
)
