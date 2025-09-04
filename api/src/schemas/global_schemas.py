from datetime import datetime
from decimal import *
import re

from pydantic.main import BaseModel
from pydantic import ValidationError, validator, constr, Json
from pydantic.networks import EmailStr
from typing import Optional, List


class GlobalFields(BaseModel):
    id: int
    created_by: Optional[str]
    created_at: datetime = datetime.utcnow()
    created_at_l: Optional[str] = None
    updated_by: Optional[str]
    updated_at: datetime = datetime.utcnow()
    updated_at_l: Optional[str] = None

    class Config:
        from_attributes = True


class Pagination(BaseModel):
    skip: Optional[int] = 0
    limit: Optional[int] = None
    order_desc: Optional[bool] = False
    sort_by: Optional[str] = 'id'


class GlobalFilters(BaseModel):
    id: int
    created_at_ini: datetime
    created_at_end: datetime
    updated_at_ini: datetime
    updated_at_end: datetime
    pagination: Pagination


class Message(BaseModel):
    status: str = "success"
    detail: Optional[str] = None

class BaseFilter(BaseModel):
    skip: Optional[int] = 0
    limit: Optional[int] = 10
    order_by: Optional[str] = 'id'
    order_desc: Optional[bool] = False

    def filter_dict(self) -> dict:
        return self.model_dump(
            exclude={"limit", "skip", "order_by", "order_desc"},
            exclude_none=True
        )