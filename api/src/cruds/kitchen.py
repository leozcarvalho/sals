from sqlalchemy.orm import Session
from src.domain.kitchen import Kitchen
from src.cruds.repo import Repository
from src.cruds.device_pins import DevicePinRepository
from src.domain import exceptions as exc

class KitchenRepository(Repository):
    def __init__(self, session: Session):
        super().__init__(Kitchen, session)
        self.device_pin_repo = DevicePinRepository(session)

    def __check_used_pins(self, values):
        pin_fields = ['shaker_pin_id', 'pump_pin_id', 'scale_pin_id', 'product_pin_id']
        for field in pin_fields:
            if self.device_pin_repo.is_pin_in_use(values[field]):
                raise exc.InvalidData(f"Pin {values[field]} is already in use.")

    def __check_is_duplicated(self, values):
        '''verificar se o mesmo se ha id duplicado em values'''
        ids = [values[field] for field in ['shaker_pin_id', 'pump_pin_id', 'scale_pin_id', 'product_pin_id'] if field in values]
        if len(ids) != len(set(ids)):
            raise exc.InvalidData("Não é permitido usar o mesmo pino em mais de uma função.")

    def save(self, values, actor=None):
        self.__check_used_pins(values)
        self.__check_is_duplicated(values)
        return super().save(values, actor)

    def update(self, id: int, values: dict, actor=None):
        self.__check_is_duplicated(values)
        return super().update(id, values, actor)
