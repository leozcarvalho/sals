from sqlmodel import Session
from src.cruds.repo import Repository
from src.domain.product import Product

class ProductRepository(Repository):
    def __init__(self, db_session: Session):
        super().__init__(Product, db_session)