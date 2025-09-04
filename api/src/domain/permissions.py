from enum import Enum

class PermissionEnum(str, Enum):
    MANAGE_USER = "manage_user"
    MANAGE_PROFILE = "create_profile"
    MANAGE_DEVICE = "manage_device"
    MANAGE_KITCHEN = "manage_kitchen"
    MANAGE_SHED = "manage_shed"
    MANAGE_STALL = "manage_stall"
    MANAGE_FEEDER = "manage_feeder"
    MANAGE_ROOM = "manage_room"
    MANAGE_INSTALATION = "manage_instalation"
    MANAGE_HARDWARE_KIND = "manage_hardware_kind"
    MANAGE_HARDWARE_DEVICE = "manage_hardware_device"
    MANAGE_HARDWARE_POINT_TYPE = "manage_hardware_point_type"
    MANAGE_HARDWARE_CONNECTION_TEMPLATE = "manage_hardware_connection_template"
    MANAGE_DEVICE_PIN = "manage_device_pin"
    MANAGE_FEEDER_VALVE = "manage_feeder_valve"

    @property
    def label(self) -> str:
        labels = {
            "manage_user": "Gerenciar Usuários",
            "create_profile": "Gerenciar Perfis",
            "manage_device": "Gerenciar Dispositivos",
            "manage_kitchen": "Gerenciar Cozinhas",
            "manage_shed": "Gerenciar Galpões",
            "manage_stall": "Gerenciar Baias",
            "manage_feeder": "Gerenciar Alimentadores",
            "manage_room": "Gerenciar Salas",
            "manage_instalation": "Gerenciar Instalações",
            "manage_hardware_kind": "Gerenciar Tipos de Hardware",
            "manage_hardware_device": "Gerenciar Dispositivos de Hardware",
            "manage_hardware_point_type": "Gerenciar Tipos de Pontos de Hardware",
            "manage_hardware_connection_template": "Gerenciar Templates de Conexão",
            "manage_device_pin": "Gerenciar Pinos de Dispositivos",
            "manage_feeder_valve": "Gerenciar Válvulas de Alimentadores",
        }
        return labels[self.value]