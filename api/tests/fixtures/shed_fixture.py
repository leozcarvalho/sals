from src.cruds.shed import ShedRepository
from src.schemas.shed import ShedCreate

SHED = ShedCreate(
    name="Galpão Principal",
)

def create_shed(session, actor=None, **overrides):
    repo = ShedRepository(session)
    shed_dict = SHED.model_dump()
    shed_dict.update(overrides)
    shed = ShedCreate(**shed_dict)
    shed = repo.save(shed.model_dump(), actor=actor)
    return shed
