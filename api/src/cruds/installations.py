from datetime import datetime, timezone
from urllib.parse import urlencode

from sqlalchemy.orm import Session

from src.domain import Installation
from src.cruds.repo import Repository
from src.cruds.hardware_device import HardwareDeviceRepository
from src.cruds.device_pins import DevicePinRepository
from src.adapters.device_adapter import DeviceService
from src.schemas.users import UserBase
from src.schemas.device_pins import DevicePinCreate
from src.domain import exceptions as exc

class InstallationRepository(Repository):
    def __init__(self, session: Session):
        super().__init__(Installation, session)
        self.device_pin_repo = DevicePinRepository(session)

    def create_pins(self, installation_id: int, device_id: int, actor=None):
        hardware_device_repo = HardwareDeviceRepository(self.db_session)
        device = hardware_device_repo.check_exists(device_id)
        connection_type = device.point_type
        for quantity in range(connection_type.points_quantity):
            pin_data = DevicePinCreate(
                installation_id=installation_id,
                number=quantity + 1,
                name=f"D{device.id}P{quantity + 1}",
                is_active=False,
            )
            self.device_pin_repo.save(pin_data.model_dump(), actor)

    def save(self, values, actor=None):
        installation = super().save(values, actor)
        self.create_pins(installation.id, installation.device_id, actor)
        return installation

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

    def _handle_device_response(self, response, id: int, actor: UserBase):
        if response.success:
            self.set_online_device(id, actor)
            return True
        self.set_offline_device(id, actor)
        raise exc.NotFound("Dispositivo offline ou inacessível.")

    def health_check(self, id: int, actor: UserBase):
        installation = self.check_exists(id)
        device_service = DeviceService(ip=installation.ip_address)
        response = device_service.healthcheck()
        return self._handle_device_response(response, id, actor)

    def restart_device(self, id: int, actor: UserBase):
        installation = self.check_exists(id)
        device_service = DeviceService(ip=installation.ip_address)
        response = device_service.restart()
        self.device_pin_repo.deactivate_all_pins(installation.id, actor)
        return self._handle_device_response(response, id, actor)

    def toggle_pin(self, id: int, pin_id: int, actor: UserBase):
        installation = self.check_exists(id)
        self.device_pin_repo.toggle_pin(pin_id, actor)
        installation = self.get(id, actor)
        device_service = DeviceService(ip=installation.ip_address)
        response = device_service._request(path=urlencode({'valvula1': installation.decimal_value, 'valvula2': 0}))
        return self._handle_device_response(response, id, actor)
