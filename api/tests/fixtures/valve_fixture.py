from decimal import Decimal
from src.cruds.valves import ValveRepository
from src.schemas.valves import ValveCreate

VALVE = ValveCreate(
    name="Válvula 1",
    device_pin_id=1,
    baia_id=1,
    max_weight=Decimal("1000.00")
)

def create_valve(session, actor=None, **overrides):
    repo = ValveRepository(session)
    valve_dict = VALVE.model_dump()
    valve_dict.update(overrides)
    valve = ValveCreate(**valve_dict)
    valve = repo.save(valve.model_dump(), actor=actor)
    return valve
