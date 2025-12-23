from src.cruds.comedouro import ComedouroRepository
from src.schemas.comedouro import ComedouroCreate

COMEDOURO = ComedouroCreate(
    name="Comedouro 1",
    baia_id=1,
    max_weight=1000.0,
)

def create_comedouro(session, actor=None, **overrides):
    repo = ComedouroRepository(session)
    comedouro_dict = COMEDOURO.model_dump()
    comedouro_dict.update(overrides)
    comedouro = ComedouroCreate(**comedouro_dict)
    comedouro = repo.save(comedouro.model_dump(), actor=actor)
    return comedouro
