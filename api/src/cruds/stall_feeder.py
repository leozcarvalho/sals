from sqlalchemy.orm import Session
from src.domain.stall_feeder import StallFeeder
from src.cruds.repo import Repository
from src.cruds.device_pins import DevicePinRepository
from src.cruds.feeder_valves import FeederValveRepository
from src.schemas.device_pins import DevicePin

class StallFeederRepository(Repository):
    def __init__(self, session: Session):
        super().__init__(StallFeeder, session)
        self.device_pin_repo = DevicePinRepository(session)
        self.feeder_valve_repo = FeederValveRepository(session)

    def __get_feeder_pins(self, stall_feeder_id: int):
        valves = []
        stall_feeder_valves = self.feeder_valve_repo.get_list(filters={"stall_feeder_id": stall_feeder_id})
        line = {}
        for valve in stall_feeder_valves:
            line['pin'] = self.device_pin_repo.get(valve.device_pin_id)
            line['id'] = valve.id
            valves.append(line)
            line = {}
        return valves

    def get_list(self, skip = 0, limit = None, filters = {}, order_by = ..., actor=None):
        result = super().get_list(skip, limit, filters, order_by, actor)
        for feeder in result:
            feeder.device_pins = self.__get_feeder_pins(feeder.id)
        return result
