from src.cruds.trato import TratoRepository
from src.schemas.trato import TratoCreate
from decimal import Decimal

TRATO = TratoCreate(
    name="Test Trato",
    hour=12,
    percent=Decimal("75.5")
)

def create_trato(session, actor=None, **overrides):
    repo = TratoRepository(session)
    trato_dict = TRATO.model_dump()
    trato_dict.update(overrides)
    trato = TratoCreate(**trato_dict)
    trato = repo.save(trato.model_dump(), actor=actor)
    return trato
