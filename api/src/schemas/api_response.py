from pydantic import BaseModel
from typing import Generic, TypeVar, Optional

T = TypeVar("T")

class ApiResponse(BaseModel, Generic[T]):
    success: bool
    data: Optional[T]
    error: Optional[str]

class ApiResponseList(BaseModel, Generic[T]):
    count: int
    items: list[T]

class AuthResponse(ApiResponse):
    access_token: str
