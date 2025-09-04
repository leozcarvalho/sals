from datetime import datetime, timezone
from urllib.parse import urlencode

from sqlalchemy.orm import Session

from src.domain import Instalation
from src.cruds.repo import Repository
from src.cruds.hardware_device import HardwareDeviceRepository
from src.cruds.device_pins import DevicePinRepository
from src.adapters.device_adapter import DeviceService
from src.schemas.users import UserBase
from src.schemas.device_pins import DevicePinCreate
from src.domain import exceptions as exc

class InstalationRepository(Repository):
    def __init__(self, session: Session):
        super().__init__(Instalation, session)
        self.device_pin_repo = DevicePinRepository(session)

    def create_pins(self, instalation_id: int, device_id: int, actor=None):
        hardware_device_repo = HardwareDeviceRepository(self.db_session)
        device = hardware_device_repo.check_exists(device_id)
        connection_type = device.point_type
        for quantity in range(connection_type.points_quantity):
            pin_data = DevicePinCreate(
                instalation_id=instalation_id,
                number=quantity + 1,
                name=f"D{device.id}P{quantity + 1}",
                is_active=False,
            )
            self.device_pin_repo.save(pin_data.model_dump(), actor)

    def get(self, id, actor=None):
        instalation = super().get(id, actor)
        decimal_value, binary_string = self.device_pin_repo.get_pins_binary_and_decimal(instalation.id)
        instalation.decimal_value = decimal_value
        instalation.binary_value = binary_string
        return instalation

    def save(self, values, actor=None):
        instalation = super().save(values, actor)
        self.create_pins(instalation.id, instalation.device_id, actor)
        return instalation

    def set_online_device(self, id: int, actor: UserBase):
        values = {
            "last_seen": datetime.now(timezone.utc),
            "is_online": True
        }
        return self.update(id, values, actor)
    
    def set_offline_device(self, id: int, actor: UserBase):
        values = {
            "is_online": False
        }
        return self.update(id, values, actor)

    def health_check(self, id: int, actor: UserBase):
        instalation = self.check_exists(id)

        device_service = DeviceService(
            ip=instalation.ip_address,
        )

        response = device_service.healthcheck()

        if response.success:
            self.set_online_device(id, actor)
            return True

        self.set_offline_device(id, actor)
        raise exc.NotFound("Dispositivo offline ou inacessível.")

    def restart_device(self, id: int, actor: UserBase):
        instalation = self.check_exists(id)

        device_service = DeviceService(
            ip=instalation.ip_address,
        )

        response = device_service.restart()

        self.device_pin_repo.deactivate_all_pins(instalation.id, actor)
        if response.success:
            return True

        self.set_offline_device(id, actor)
        raise exc.NotFound("Dispositivo offline ou inacessível.")

    def toggle_pin(self, id: int, pin_id: int, actor: UserBase):
        instalation = self.check_exists(id)
        self.device_pin_repo.toggle_pin(pin_id, actor)
        instalation = self.get(id, actor)
        device_service = DeviceService(
            ip=instalation.ip_address,
        )
        response = device_service._request(path=urlencode({'valvula1': instalation.decimal_value, 'valvula2': 0}))
        if response.success:
            self.set_online_device(id, actor)
            return True
        raise exc.NotFound("Dispositivo offline ou inacessível.")
