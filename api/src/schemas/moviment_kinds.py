from pydantic.main import BaseModel
from typing import Optional
from src.schemas.global_schemas import BaseFilter, GlobalFields


class MovimentKindBase(BaseModel):
    kind: str
    code: str

class MovimentKindCreate(MovimentKindBase):
    pass

class MovimentKindUpdate(MovimentKindBase):
    pass

class MovimentKind(MovimentKindBase, GlobalFields):
    pass

class MovimentKindFilter(BaseFilter):
    kind: Optional[str] = None
