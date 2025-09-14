from typing import List
from sqlalchemy.orm import Session
from src.domain.kitchen import Kitchen
from src.cruds.repo import Repository
from src.cruds.device_pins import DevicePinRepository
from src.cruds.kitchen_products import KitchenProductRepository
from src.schemas.kitchen_products import KitchenProductCreate
from src.schemas.kicthen import KitchenCreate, KitchenUpdate
from src.domain import exceptions as exc

class KitchenRepository(Repository):
    def __init__(self, session: Session):
        super().__init__(Kitchen, session)
        self.device_pin_repo = DevicePinRepository(session)
        self.kitchen_product_repo = KitchenProductRepository(session)

    def __check_used_pins(self, values):
        pin_fields = ['shaker_pin_id', 'pump_pin_id', 'scale_pin_id']
        for field in pin_fields:
            self.device_pin_repo._is_valid_pin(values[field])

    def __check_is_duplicated(self, values):
        ids = [values[field] for field in ['shaker_pin_id', 'pump_pin_id', 'scale_pin_id'] if field in values]
        if len(ids) != len(set(ids)):
            raise exc.InvalidData("Não é permitido usar o mesmo pino em mais de uma função.")

    def save(self, values, actor=None):
        self.__check_used_pins(values)
        self.__check_is_duplicated(values)
        products = values.pop("products", []) or []
        kitchen = super().save(values, actor)
        self.__update_product_pins(kitchen.id, products, actor)
        return kitchen

    def update(self, id: int, values: dict, actor=None):
        self.__check_is_duplicated(values)
        products = values.pop("products", []) or []
        kitchen = super().update(id, values, actor)
        self.__update_product_pins(kitchen.id, products, actor)
        return kitchen

    def __update_product_pins(self, kitchen_id: int, products: List[KitchenProductCreate], actor=None):
        ids = [product['device_pin_id'] for product in products]
        if len(ids) != len(set(ids)):
            raise exc.InvalidData("Não é permitido usar o mesmo pino em mais de uma função.")

        self.kitchen_product_repo.delete_by_kitchen_id(kitchen_id)
        for product in products:
            self.device_pin_repo._is_valid_pin(product['device_pin_id'])
            values = dict(
                kitchen_id=kitchen_id,
                device_pin_id=product['device_pin_id']
            )
            self.kitchen_product_repo.save(values, actor)
