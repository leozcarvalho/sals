from src.cruds.kitchen import KitchenRepository
from src.schemas.kicthen import KitchenCreate

KITCHEN = KitchenCreate(
    name="CZ2",
    shaker_pin_id=1,
    pump_pin_id=2,
    scale_pin_id=3,
    volume_misturador=2000,
    fracao_volume_misturador=95,
)

def create_kitchen(session, actor=None, **overrides):
    repo = KitchenRepository(session)
    kitchen_dict = KITCHEN.model_dump()
    kitchen_dict.update(overrides)
    kitchen = KitchenCreate(**kitchen_dict)
    kitchen = repo.save(kitchen.model_dump(), actor=actor)
    return kitchen

