from sqlmodel import Session
from src.cruds.repo import Repository
from src.domain.product import Product
from src.domain import exceptions as exc

class ProductRepository(Repository):
    def __init__(self, db_session: Session):
        super().__init__(Product, db_session)
    
    def delete(self, id, actor=None):
        product = self.check_exists(id)
        if str(product.name.upper()) == "ÁGUA":
            raise exc.InvalidData("Água não pode ser excluída")
        return super().delete(id, actor)