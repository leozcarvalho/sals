from sqlmodel import Session
from src.cruds.repo import Repository
from src.domain.product import Product
from src.domain import exceptions as exc

class ProductRepository(Repository):
    def __init__(self, db_session: Session):
        super().__init__(Product, db_session)
    
    def block_water(self, product):
        if str(product.name.upper()) == "ÁGUA":
            raise exc.InvalidData("Água não pode ser modificada")

    def update(self, id, values, actor=None):
        product = self.check_exists(id)
        self.block_water(product)
        return super().update(id, values, actor)
    
    def delete(self, id, actor=None):
        product = self.check_exists(id)
        self.block_water(product)
        return super().delete(id, actor)