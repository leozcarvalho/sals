from src.cruds.baia import BaiaRepository
from src.schemas.baia import BaiaCreate

BAIA = BaiaCreate(
    name="Baia 1",
    sala_id=1
)

def create_baia(session, actor=None, **overrides):
    repo = BaiaRepository(session)
    baia_dict = BAIA.model_dump()
    baia_dict.update(overrides)
    baia = BaiaCreate(**baia_dict)
    baia = repo.save(baia.model_dump(), actor=actor)
    return baia
