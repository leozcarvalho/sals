from src.cruds.room_stall import RoomStallRepository
from src.schemas.room_stall import RoomStallCreate

ROOM_STALL = RoomStallCreate(
    name="Baia 1",
    shed_room_id=1
)

def create_room_stall(session, actor=None, **overrides):
    repo = RoomStallRepository(session)
    room_stall_dict = ROOM_STALL.model_dump()
    room_stall_dict.update(overrides)
    room_stall = RoomStallCreate(**room_stall_dict)
    room_stall = repo.save(room_stall.model_dump(), actor=actor)
    return room_stall
