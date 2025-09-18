import pytest
from src.cruds.stall_feeder import StallFeederRepository
from src.schemas.stall_feeder import StallFeederCreate

STALL_FEEDER = StallFeederCreate(
    name="Comedouro 1",
    room_stall_id=1,
    max_weight=1000.0,
)

def create_stall_feeder(session, actor=None, **overrides):
    repo = StallFeederRepository(session)
    stall_feeder_dict = STALL_FEEDER.model_dump()
    stall_feeder_dict.update(overrides)
    stall_feeder = StallFeederCreate(**stall_feeder_dict)
    stall_feeder = repo.save(stall_feeder.model_dump(), actor=actor)
    return stall_feeder
