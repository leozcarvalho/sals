import pytest
from src.cruds.batch import BatchRepository
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
