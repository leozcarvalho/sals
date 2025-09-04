from pydantic.main import BaseModel
from typing import Optional
from src.schemas.global_schemas import BaseFilter, GlobalFields

class ProfileBase(BaseModel):
    name: str
    permissions: list[str] = []


class ProfileCreate(ProfileBase):
    pass

class ProfileUpdate(ProfileBase):
    pass

class ProfileRead(ProfileBase, GlobalFields):
    pass

class ProfileFilter(BaseFilter):
    kind: Optional[str] = None
