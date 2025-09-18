import pytest
from src.cruds.shed_room import ShedRoomRepository
from src.schemas.shed_room import ShedRoomCreate

SHED_ROOM = ShedRoomCreate(
    name="Sala 1",
    shed_id=1,
    entrance_pin_id=1,
)

def create_shed_room(session, actor=None, **overrides):
    repo = ShedRoomRepository(session)
    shed_room_dict = SHED_ROOM.model_dump()
    shed_room_dict.update(overrides)
    shed_room = ShedRoomCreate(**shed_room_dict)
    shed_room = repo.save(shed_room.model_dump(), actor=actor)
    return shed_room
