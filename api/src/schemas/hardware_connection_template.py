from pydantic.main import BaseModel
from typing import Optional
from src.schemas.global_schemas import BaseFilter, GlobalFields

class HardwareConnectionTemplateBase(BaseModel):
    name: str
    template_url: str
    query_string: str

class HardwareConnectionTemplateCreate(HardwareConnectionTemplateBase):
    pass

class HardwareConnectionTemplateUpdate(HardwareConnectionTemplateBase):
    pass

class HardwareConnectionTemplate(HardwareConnectionTemplateBase, GlobalFields):
    pass

class HardwareConnectionTemplateFilter(BaseFilter):
    name: Optional[str] = None
    template_url: Optional[str] = None
