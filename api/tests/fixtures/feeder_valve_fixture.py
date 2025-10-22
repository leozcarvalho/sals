from src.cruds.feeder_valves import FeederValveRepository
from src.schemas.feeder_valves import FeederValveCreate

FEEDER_VALVE = FeederValveCreate(
    device_pin_id=1,
    stall_feeder_id=1
)

def create_feeder_valve(session, actor=None, **overrides):
    repo = FeederValveRepository(session)
    feeder_valve_dict = FEEDER_VALVE.model_dump()
    feeder_valve_dict.update(overrides)
    feeder_valve = FeederValveCreate(**feeder_valve_dict)
    feeder_valve = repo.save(feeder_valve.model_dump(), actor=actor)
    return feeder_valve
