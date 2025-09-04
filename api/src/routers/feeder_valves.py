from fastapi import Depends
from src.routers.base_router import BaseRouter
from src.schemas.feeder_valves import FeederValve, FeederValveCreate, FeederValveUpdate, FeederValveFilter
from src.cruds.feeder_valves import FeederValveRepository
from src.core.db import get_session
from src.routers.dependencies import get_current_user


def get_feeder_valve_service(session = Depends(get_session)):
    return FeederValveRepository(session)

router_feeder_valves = BaseRouter(
    prefix="/feeder-valves",
    read_schema=FeederValve,
    create_schema=FeederValveCreate,
    update_schema=FeederValveUpdate,
    filter_schema=FeederValveFilter,
    get_service=get_feeder_valve_service,
    get_current_user=get_current_user,
    tags=["Feeder Valves"]
)
