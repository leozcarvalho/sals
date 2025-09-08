from pydantic.networks import EmailStr
from pydantic import BaseModel, Json
from src.schemas.global_schemas import GlobalFields, BaseFilter
from typing import Optional


class UserBase(BaseModel):
    email: str
    name: str
    is_active: Optional[bool] = True
    profile_id: int


class UserBaseData(UserBase):
    password: str

class UserCreate(UserBaseData):
    pass

class UserUpdate(UserBaseData):
    pass

class UserRead(GlobalFields, UserBase):
    pass

class UserFilter(BaseFilter):
    email: Optional[str] = None
    name: Optional[str] = None
    is_active: Optional[bool] = None
    profile_id: Optional[int] = None