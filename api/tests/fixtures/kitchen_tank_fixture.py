import pytest
from src.cruds.kitchen_tanks import KitchenTankRepository
from src.schemas.kitchen_tanks import KitchenTankCreate

KITCHEN_TANK = KitchenTankCreate(
    product_tank_id=1,
    kitchen_id=1
)

def create_kitchen_tank(session, actor=None, **overrides):
    repo = KitchenTankRepository(session)
    data = KITCHEN_TANK.model_dump()
    data.update(overrides)
    kitchen_tank = repo.save(data, actor=actor)
    return kitchen_tank