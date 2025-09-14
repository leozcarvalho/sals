from pydantic.main import BaseModel
from typing import Optional
from src.schemas.global_schemas import BaseFilter, GlobalFields

class DevicePinBase(BaseModel):
    name: str
    mode: Optional[str] = "output"  # "input" ou "output"
    svg_region_id: Optional[str] = None
    activation_color: Optional[str] = None
    is_active: Optional[bool] = False

class DevicePinCreate(DevicePinBase):
    number: int
    installation_id: int

class DevicePinUpdate(DevicePinBase):
    pass

class DevicePin(DevicePinCreate, GlobalFields):
    is_active: bool
    in_use: Optional[bool] = False
    installation_name: Optional[str] = None


class DevicePinFilter(BaseFilter):
    name: Optional[str] = None
    installation_id: Optional[int] = None
    number: Optional[int] = None
    is_active: Optional[bool] = None
    mode: Optional[str] = None
    in_use: Optional[bool] = None

