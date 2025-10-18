from pydantic.main import BaseModel
from typing import Optional
from src.schemas.global_schemas import BaseFilter, GlobalFields
from src.schemas.hardware_connection_template import HardwareConnectionTemplate
from src.schemas.hardware_kind import HardwareKind
from src.schemas.hardware_point_types import HardwarePointType

class HardwareDeviceBase(BaseModel):
    name: str
    connection_template_id: int
    hardware_kind_id: int
    point_type_id: int

class HardwareDeviceCreate(HardwareDeviceBase):
    pass

class HardwareDeviceUpdate(HardwareDeviceBase):
    pass

class HardwareDevice(HardwareDeviceBase, GlobalFields):
    connection_template: HardwareConnectionTemplate
    hardware_kind: HardwareKind
    point_type: HardwarePointType

class HardwareDeviceFilter(BaseFilter):
    name: Optional[str] = None
    connection_template_id: Optional[int] = None
    hardware_kind_id: Optional[int] = None
    point_type_id: Optional[int] = None
