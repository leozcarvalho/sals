from src.cruds.batch import BatchRepository
from src.schemas.batch import BatchCreate

BATCH = BatchCreate(
    name="Lote 1",
    description="Lote inicial",
    initial_day=1,
    is_active=True,
    feeding_curve_id=1,
    shed_id=1,
    shed_room_id=1,
)

def create_batch(session, actor=None, **overrides):
    repo = BatchRepository(session)
    data = BATCH.model_dump()
    data.update(overrides)
    batch = repo.save(data, actor=actor)
    return batch
