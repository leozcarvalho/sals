from src.cruds.moviment_kinds import MovimentKindRepository
from src.schemas.moviment_kinds import MovimentKindBase

MOVIMENT_KIND = MovimentKindBase(
    kind="tipo_1",
    code="Descrição do Tipo 1"
)

def create_moviment_kind(session, actor=None, **overrides):
    repo = MovimentKindRepository(session)
    data = MOVIMENT_KIND.model_dump()
    data.update(overrides)
    moviment_kind = repo.save(data, actor=actor)
    return moviment_kind
