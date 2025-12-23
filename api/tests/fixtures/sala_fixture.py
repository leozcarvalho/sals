from src.cruds.sala import SalaRepository
from src.schemas.sala import SalaCreate

SALA = SalaCreate(
    name="Sala 1",
    shed_id=1,
    entrance_pin_id=1,
)

def create_sala(session, actor=None, **overrides):
    repo = SalaRepository(session)
    sala_dict = SALA.model_dump()
    sala_dict.update(overrides)
    sala = SalaCreate(**sala_dict)
    sala = repo.save(sala.model_dump(), actor=actor)
    return sala
