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
