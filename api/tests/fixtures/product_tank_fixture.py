from src.cruds.product_tank import ProductTankRepository
from src.schemas.product_tank import ProductTankCreate

PRODUCT_TANK = ProductTankCreate(
    name="Tanque Principal",
    description="Tanque para água",
    screw_pin_id=1,
    product_id=1,
    volume=10000,
    is_dosador_seco=False,
)

def create_product_tank(session, actor=None, **overrides):
    repo = ProductTankRepository(session)
    data = PRODUCT_TANK.model_dump()
    data.update(overrides)
    product_tank = repo.save(data, actor=actor)
    return product_tank