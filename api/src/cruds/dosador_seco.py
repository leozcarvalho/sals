from sqlalchemy.orm import Session
from src.cruds.repo import Repository
from src.domain import Kitchen, Valve
from src.domain import exceptions as exc
from src.domain import DosadorSeco
from src.cruds.device_pins import DevicePinRepository
from src.schemas.device_pins import DevicePin as DevicePinSchema

class DosadorSecoRepository(Repository):
    def __init__(self, session: Session):
        super().__init__(DosadorSeco, session)
        self.device_pin_repo = DevicePinRepository(session)

    def __check_used_pins(self, values):
        pin_fields = ['output_pin_id', 'scale_pin_id']
        for field in pin_fields:
            if values[field]:
                self.device_pin_repo._is_valid_pin(values[field])

    def __check_is_duplicated(self, values):
        ids = [values[field] for field in ['output_pin_id', 'scale_pin_id'] if field in values and values[field] is not None]
        if len(ids) != len(set(ids)):
            raise exc.InvalidData("Não é permitido usar o mesmo pino em mais de uma função.")

    def save(self, values, actor=None):
        self.__check_used_pins(values)
        self.__check_is_duplicated(values)
        return super().save(values, actor)

    def update(self, id: int, values: dict, actor=None):
        self.__check_is_duplicated(values)
        return super().update(id, values, actor)
