from datetime import datetime, timezone
from typing import List

from sqlalchemy.orm import Session

from src.domain import Installation
from src.cruds.repo import Repository
from src.cruds.hardware_device import HardwareDeviceRepository
from src.cruds.device_pins import DevicePinRepository
from src.adapters.device_adapter import DeviceService
from src.schemas.users import UserBase
from src.schemas.device_pins import DevicePinCreate, DevicePinBulkUpdate
from src.domain import exceptions as exc


class InstallationRepository(Repository):
    # Cache compartilhado entre todas as instâncias
    _device_services = {}  # chave: ip, valor: DeviceService

    def __init__(self, session: Session):
        super().__init__(Installation, session)
        self.device_pin_repo = DevicePinRepository(session)

    # ---------- DeviceService ----------

    @classmethod
    def _get_device_service(cls, installation: Installation) -> DeviceService:
        """
        Retorna um DeviceService para a instalação. Cria se não existir.
        """
        if installation.ip_address not in cls._device_services:
            cls._device_services[installation.ip_address] = DeviceService(
                ip=installation.ip_address,
                url_template=installation.device.connection_template.template_url,
                query_string=installation.device.connection_template.query_string
            )
        return cls._device_services[installation.ip_address]

    @classmethod
    def close_all_device_sessions(cls):
        """
        Fecha todas as sessões de DeviceService compartilhadas.
        """
        for ds in cls._device_services.values():
            ds.session.close()
        cls._device_services.clear()

    # ---------- CRUD e Pins ----------

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
    
    def update_device_pins(self, installation_id: int, device_pins: List[DevicePinBulkUpdate], actor=None):
        self.check_exists(installation_id)
        for pin_data in device_pins:
            self.device_pin_repo.update(pin_data.id, pin_data.model_dump(exclude={"id"}), actor)
        return True

    # ---------- Device Status ----------

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

    def _handle_response(self, response, id: int, method: str, actor: UserBase):
        self._handle_device_response(response, id, actor)
        match method:
            case "restart":
                self.device_pin_repo.deactivate_all_pins(id, actor)

    def exec_action(self, id: int, action: str, actor= None, **kwargs):
        """
        Executa uma ação genérica em uma instalação.
        
        :param id: ID da instalação
        :param action: nome do método a ser executado no DeviceService
                       ex: 'healthcheck', 'tare', 'restart', 'calibrate', 'send_value', 'read_value'
        :param actor: usuário que executa a ação
        :param kwargs: parâmetros adicionais para o método (ex: weight, value)
        """
        installation = self.check_exists(id)
        device_service = self._get_device_service(installation)
        method = getattr(device_service, action, None)
        if not method:
            raise exc.NotFound(f"Ação '{action}' não encontrada no DeviceService")
        try:
            response = method(**kwargs) if kwargs else method()
        except Exception as e:
            raise exc.ConnectionError(f"Falha ao executar '{action}' no dispositivo {installation.ip_address}: {e}")
        self._handle_response(response, id, action, actor)
        return response
