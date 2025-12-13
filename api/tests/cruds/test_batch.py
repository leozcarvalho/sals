import pytest
from src.cruds.batch import BatchRepository
from src.cruds.shed_room import ShedRoomRepository

from tests.fixtures.batch_fixture import create_batch, BATCH
from tests.fixtures.feeding_curve_fixture import create_feeding_curve
from tests.fixtures.shed_fixture import create_shed
from tests.fixtures.shed_room_fixture import create_shed_room

def test_create_batch(session):
    repo = BatchRepository(session)
    data = BATCH.model_dump()
    feeding_curve = create_feeding_curve(session)
    data["feeding_curve_id"] = feeding_curve.id
    shed = create_shed(session)
    data["shed_id"] = shed.id
    shed_room = create_shed_room(session, shed_id=shed.id)
    data["shed_room_id"] = shed_room.id
    batch = repo.save(data)
    assert batch.id is not None
    assert batch.name == data["name"]

def test_get_batch(session):
    batch = create_batch(session)
    repo = BatchRepository(session)
    fetched = repo.get(batch.id)
    assert fetched is not None
    assert fetched.id == batch.id
    assert fetched.name == batch.name

def test_update_batch(session):
    batch = create_batch(session)
    repo = BatchRepository(session)
    data = { "name": "Updated Batch Name" }
    updated = repo.update(batch.id, data)
    assert updated.name == data["name"]

def test_delete_batch(session):
    batch = create_batch(session)
    repo = BatchRepository(session)
    repo.delete(batch.id)
    fetched = repo.get(batch.id)
    assert fetched is None

def test_list_batches(session):
    batch1 = create_batch(session, name="Batch 1")
    batch2 = create_batch(session, name="Batch 2")
    repo = BatchRepository(session)
    batches = repo.get_list()
    batch_names = [batch.name for batch in batches]
    assert "Batch 1" in batch_names
    assert "Batch 2" in batch_names


#testar filtro is_in_batch
def test_shed_room_is_in_batch_filter(session):
    shed = create_shed(session)
    shed_room1 = create_shed_room(session, shed_id=shed.id, name="SALA 1")
    create_shed_room(session, shed_id=shed.id, name="SALA 2")
    feeding_curve = create_feeding_curve(session)
   
    # Criar um lote associado à shed_room1
    create_batch(session, shed_room_id=shed_room1.id, shed_id=shed.id, feeding_curve_id=feeding_curve.id, name="Batch for Shed Room 1")
    
    shed_room_repo = ShedRoomRepository(session)

    # Filtrar por salas que estão em lote
    filters_in_batch = { "is_in_batch": True }
    rooms_in_batch = shed_room_repo.get_list(filters=filters_in_batch)
    room_names_in_batch = [room.name for room in rooms_in_batch]
    assert "SALA 1" in room_names_in_batch
    assert "SALA 2" not in room_names_in_batch

    # Filtrar por salas que não estão em lote
    filters_not_in_batch = { "is_in_batch": False }
    rooms_not_in_batch = shed_room_repo.get_list(filters=filters_not_in_batch)
    room_names_not_in_batch = [room.name for room in rooms_not_in_batch]
    assert "SALA 1" not in room_names_not_in_batch
    assert "SALA 2" in room_names_not_in_batch
