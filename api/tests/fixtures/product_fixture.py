from src.cruds.product import ProductRepository
from src.schemas.product import ProductCreate

PRODUCT = ProductCreate(
    name="Água",
    description="Água natural",
    moisture_percentage=0,
    kind="liquid",
    density=1000,
    is_active=True
)

def create_product(session, actor=None, **overrides):
    repo = ProductRepository(session)
    data = PRODUCT.model_dump()
    data.update(overrides)
    product = repo.save(data, actor=actor)
    return product
