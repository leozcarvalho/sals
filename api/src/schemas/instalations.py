from datetime import datetime
from pydantic import BaseModel
from src.schemas.global_schemas import GlobalFields, BaseFilter
from typing import Optional, List
from src.schemas.hardware_device import HardwareDevice
from src.schemas.device_pins import DevicePin

class InstalationBase(BaseModel):
    ip_address: str
    name: str
    last_seen: Optional[datetime] = None
    is_online: bool = False
    device_id: int

class InstalationCreate(InstalationBase):
    pass

class InstalationUpdate(InstalationBase):
    pass

class Instalation(GlobalFields, InstalationBase):
    device: HardwareDevice
    pins: List[DevicePin] = []
    binary_value: Optional[str] = None
    decimal_value: Optional[int] = None


class InstalationFilter(BaseFilter):
    ip_address: Optional[str] = None
    name: Optional[str] = None
    is_online: Optional[bool] = None
    device_id: Optional[int] = None
