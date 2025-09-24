from fastapi import Depends
from src.routers.base_router import BaseRouter
from src.schemas.formula import FormulaRead, FormulaCreate, FormulaUpdate, FormulaFilter
from src.cruds.formula import FormulaRepository
from src.core.db import get_session
from src.routers.dependencies import get_current_user
from src.domain.permissions import PermissionEnum

def get_formula_service(session = Depends(get_session)):
    return FormulaRepository(session)

router_formulas = BaseRouter(
    prefix="/formulas",
    read_schema=FormulaRead,
    create_schema=FormulaCreate,
    update_schema=FormulaUpdate,
    filter_schema=FormulaFilter,
    get_service=get_formula_service,
    get_current_user=get_current_user,
    tags=["Formulas"],
    default_permission=PermissionEnum.MANAGE_FORMULA,
)