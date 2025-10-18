from enum import Enum

class PermissionEnum(str, Enum):
    MANAGE_USER = "manage_user"
    MANAGE_PROFILE = "manage_profile"
    MANAGE_DEVICE = "manage_device"
    MANAGE_KITCHEN = "manage_kitchen"
    MANAGE_SHED = "manage_shed"
    MANAGE_STALL = "manage_stall"
    MANAGE_ROOM = "manage_room"
    MANAGE_INSTALLATION = "manage_installation"
    MANAGE_HARDWARE_KIND = "manage_hardware_kind"
    MANAGE_HARDWARE_DEVICE = "manage_hardware_device"
    MANAGE_HARDWARE_POINT_TYPE = "manage_hardware_point_type"
    MANAGE_HARDWARE_CONNECTION_TEMPLATE = "manage_hardware_connection_template"
    MANAGE_DEVICE_PIN = "manage_device_pin"
    MANAGE_FEEDER_VALVE = "manage_feeder_valve"
    MANAGE_SHED_ROOM = "manage_shed_room"
    MANAGE_ROOM_STALL = "manage_room_stall"
    MANAGE_STALL_FEEDER = "manage_stall_feeder"
    MANAGE_HEALTHCHECK_PRIORITY = "manage_healthcheck_priority"
    MANAGE_PRODUCT = "manage_product"
    MANAGE_PRODUCT_TANK = "manage_product_tank"
    MANAGE_KITCHEN_TANK = "manage_kitchen_tank"
    MANAGE_FORMULA = "manage_formula"
    MANAGE_FEEDING_CURVE = "manage_feeding_curve"
    MANAGE_SVG = "manage_svg"

    @property
    def label(self) -> str:
        labels = {
            "manage_user": "Gerenciar Usuários",
            "manage_profile": "Gerenciar Perfis",
            "manage_device": "Gerenciar Dispositivos",
            "manage_kitchen": "Gerenciar Cozinhas",
            "manage_room": "Gerenciar Salas",
            "manage_installation": "Gerenciar Instalações",
            "manage_hardware_kind": "Gerenciar Tipos de Hardware",
            "manage_hardware_device": "Gerenciar Dispositivos de Hardware",
            "manage_hardware_point_type": "Gerenciar Tipos de Pontos de Hardware",
            "manage_hardware_connection_template": "Gerenciar Templates de Conexão",
            "manage_device_pin": "Gerenciar Pinos de Dispositivos",
            "manage_feeder_valve": "Gerenciar Válvulas de Alimentadores",
            "manage_shed_room": "Gerenciar Salas",
            "manage_room_stall": "Gerenciar Baias",
            "manage_stall_feeder": "Gerenciar Comedouros",
            "manage_shed": "Gerenciar Galpões",
            "manage_stall": "Gerenciar Baias",
            "manage_healthcheck_priority": "Gerenciar Prioridades de Healthcheck",
            "manage_product": "Gerenciar Produtos",
            "manage_product_tank": "Gerenciar Tanques de Produto",
            "manage_kitchen_tank": "Gerenciar Tanques da Cozinha",
            "manage_formula": "Gerenciar Fórmulas",
            "manage_feeding_curve": "Gerenciar Curvas de Alimentação",
            "manage_svg": "Gerenciar SVGs",
        }
        return labels[self.value]
