from fastapi import APIRouter, Depends
from pydantic import BaseModel

from src.core.db import get_session
from src.routers.dependencies import get_current_user
from src.schemas.api_response import ApiResponse
from src.cruds.scripts import exec_script

class ScriptRequest(BaseModel):
    script_name: str
    params: dict

router_scripts = APIRouter(prefix="/scripts", tags=["Scripts"])

@router_scripts.post("/script-1")
def run_script_1(data: ScriptRequest, current_user = Depends(get_current_user), session = Depends(get_session)):
    result = exec_script(session, data.script_name, data.params)
    return ApiResponse(success=True, message="Script executed successfully", data=result)
