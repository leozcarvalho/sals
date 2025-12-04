import pytest
from tests.fixtures.moviment_kinds_fixture import create_moviment_kind, MOVIMENT_KIND
from src.cruds.moviment_kinds import MovimentKindRepository

@pytest.fixture
def moviment_kind_repository(session) -> MovimentKindRepository:
    return MovimentKindRepository(session)


def test_create_moviment_kind(moviment_kind_repository):
    data = MOVIMENT_KIND.model_dump()
    moviment_kind = moviment_kind_repository.save(data)
    assert moviment_kind.id is not None
    assert moviment_kind.kind == "tipo_1"

def test_update_moviment_kind(session, moviment_kind_repository, actor):
    moviment_kind = create_moviment_kind(session)
    update_data = {"kind": "tipo_atualizado", "code": "Descrição Atualizada"}
    updated_mk = moviment_kind_repository.update(moviment_kind.id, update_data, actor=actor)
    assert updated_mk.kind == "tipo_atualizado"
    assert updated_mk.code == "Descrição Atualizada"

def test_delete_moviment_kind(session, moviment_kind_repository):
    moviment_kind = create_moviment_kind(session)
    moviment_kind_repository.delete(moviment_kind.id)
    
    deleted_mk = moviment_kind_repository.get(moviment_kind.id)
    assert deleted_mk is None

def test_get_list_moviment_kinds(session, moviment_kind_repository):
    # cria alguns moviment kinds
    create_moviment_kind(session, kind="ENTRADA", code="Descrição 1")
    create_moviment_kind(session, kind="SAIDA", code="Descrição 2")

    mk_list = moviment_kind_repository.get_list()

    assert "ENTRADA" in mk_list[0].kind
    assert "SAIDA" in mk_list[1].kind
    assert len(mk_list) == 2