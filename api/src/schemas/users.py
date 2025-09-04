from pydantic.networks import EmailStr
from pydantic import BaseModel, Json
from src.schemas.global_schemas import GlobalFields, BaseFilter, Message
from typing import Optional, List


class UserBase(BaseModel):
    email: str
    name: str
    password: str
    is_active: Optional[bool] = True
    profile_id: int


class UserCreate(UserBase):
    pass

class UserUpdate(BaseModel):
    pass

class UserRead(GlobalFields, UserBase):
    pass

class UserFilter(BaseFilter):
    email: Optional[EmailStr]
    name: Optional[str]
    is_active: Optional[bool]
    profile_id: Optional[int]