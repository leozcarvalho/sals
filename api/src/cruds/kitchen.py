from typing import List
from sqlalchemy.orm import Session
from src.domain.kitchen import Kitchen
from src.cruds.repo import Repository
from src.cruds.device_pins import DevicePinRepository
from src.cruds.kitchen_tanks import KitchenTankRepository
from src.schemas.kitchen_tanks import KitchenTankCreate
from src.domain import exceptions as exc

class KitchenRepository(Repository):
    def __init__(self, session: Session):
        super().__init__(Kitchen, session)
        self.device_pin_repo = DevicePinRepository(session)
        self.kitchen_tank_repo = KitchenTankRepository(session)

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
        tanks = values.pop("tanks", []) or []
        kitchen = super().save(values, actor)
        if tanks: self.__update_tanks(kitchen.id, tanks, actor)
        return kitchen

    def update(self, id: int, values: dict, actor=None):
        self.__check_is_duplicated(values)
        tanks = values.pop("tanks", []) or []
        kitchen = super().update(id, values, actor)
        if tanks: self.__update_tanks(kitchen.id, tanks, actor)
        return kitchen

    def __update_tanks(self, kitchen_id: int, tanks: List[KitchenTankCreate], actor=None):
        self.kitchen_tank_repo.delete_by_kitchen_id(kitchen_id)
        for tank in tanks:
            values = dict(
                kitchen_id=kitchen_id,
                product_tank_id=tank['product_tank_id']
            )
            self.kitchen_tank_repo.save(values, actor)
