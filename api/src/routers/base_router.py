from fastapi import APIRouter, Depends
from pydantic import BaseModel
from typing import Generic, TypeVar, Type, List, Optional
from src.cruds.repo import Repository
from src.schemas.api_response import ApiResponse, ApiResponseList
from src.schemas.users import UserBase

ReadSchemaType = TypeVar("ReadSchemaType", bound=BaseModel)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)
FilterSchemaType = TypeVar("FilterSchemaType", bound=BaseModel)


class BaseRouter(Generic[ReadSchemaType, CreateSchemaType, UpdateSchemaType]):
    def __init__(
        self,
        prefix: str,
        read_schema: Type[ReadSchemaType],
        create_schema: Type[CreateSchemaType],
        update_schema: Type[UpdateSchemaType],
        filter_schema: Type[FilterSchemaType],
        get_service: callable,
        get_current_user: Optional[callable] = None,
        tags: List[str] = None
    ):
        self.router = APIRouter(prefix=prefix, tags=tags or [prefix.strip("/")])
        self.read_schema = read_schema
        self.create_schema = create_schema
        self.update_schema = update_schema
        self.filter_schema = filter_schema
        self.get_service = get_service
        self.get_current_user = get_current_user
        self._add_routes()

    def _add_routes(self):
        @self.router.post("", response_model=ApiResponse[self.read_schema])
        def create(data: self.create_schema, service: Repository = Depends(self.get_service), current_user: UserBase = Depends(self.get_current_user)):
            obj = service.save(data.dict(), actor=current_user)
            return ApiResponse(success=True, data=obj, error=None)

        @self.router.get("", response_model=ApiResponse[ApiResponseList[self.read_schema]])
        def list_all(
            filters: self.filter_schema = Depends(),
            service: Repository = Depends(self.get_service),
            current_user: UserBase = Depends(self.get_current_user)
        ):
            objs, count = service.get_list_and_count(actor=current_user, filters=filters.filter_dict(), skip=filters.skip, limit=filters.limit, order_by={})
            return ApiResponse(success=True, data=ApiResponseList(count=count, items=objs), error=None)

        @self.router.get("/{item_id}", response_model=ApiResponse[self.read_schema])
        def get(item_id: int, service: Repository = Depends(self.get_service), current_user: UserBase = Depends(self.get_current_user)):
            obj = service.check_exists(item_id, actor=current_user)
            return ApiResponse(success=True, data=obj, error=None)

        @self.router.put("/{item_id}", response_model=ApiResponse[self.read_schema])
        def update(item_id: int, data: self.update_schema, service: Repository = Depends(self.get_service), current_user: UserBase = Depends(self.get_current_user)):
            obj = service.update(item_id, data.dict(exclude_unset=True), actor=current_user)
            return ApiResponse(success=True, data=obj, error=None)

        @self.router.delete("/{item_id}", response_model=ApiResponse[self.read_schema])
        def delete(item_id: int, service: Repository = Depends(self.get_service), current_user: UserBase = Depends(self.get_current_user)):
            obj = service.delete(item_id, actor=current_user)
            return ApiResponse(success=True, data=obj, error=None)
