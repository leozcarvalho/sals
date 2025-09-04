from pydantic import BaseModel
from typing import Generic, TypeVar, Optional
from pydantic.generics import GenericModel

T = TypeVar("T")

class ApiResponse(GenericModel, Generic[T]):
    success: bool
    data: Optional[T]
    error: Optional[str]

class ApiResponseList(GenericModel, Generic[T]):
    count: int
    items: list[T]

class AuthResponse(ApiResponse):
    access_token: str
