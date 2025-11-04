from datetime import datetime
from pydantic import BaseModel
from src.schemas.global_schemas import GlobalFields, BaseFilter
from typing import Optional, List
from src.schemas.hardware_device import HardwareDevice
from src.schemas.device_pins import DevicePin

class InstallationBase(BaseModel):
    ip_address: str
    name: str
    last_seen: Optional[datetime] = None
    is_online: bool = False
    device_id: int
    healthcheck_priority_id: Optional[int] = None

class InstallationCreate(InstallationBase):
    pass

class InstallationUpdate(InstallationBase):
    pass

class Installation(GlobalFields, InstallationBase):
    hardware_kind: str
    device: HardwareDevice
    pins: List[DevicePin] = []
    binary_value: Optional[str] = None
    decimal_value: Optional[int] = None


class InstallationFilter(BaseFilter):
    ip_address: Optional[str] = None
    name: Optional[str] = None
    is_online: Optional[bool] = None
    device_id: Optional[int] = None
