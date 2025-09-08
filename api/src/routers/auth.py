import json
from fastapi import APIRouter, Depends, Response
from fastapi.security import OAuth2PasswordRequestForm
from src.cruds.auth import AuthService
from src.schemas.api_response import ApiResponse
from src.cruds.users import UsersRepository
from src.core.db import get_session

auth_router = APIRouter(tags=["Auth"])

def get_user_repository(session = Depends(get_session)):
    return UsersRepository(session)

@auth_router.post("/login", response_model=ApiResponse)
def login(response: Response, form_data: OAuth2PasswordRequestForm = Depends(), user_repository: UsersRepository = Depends(get_user_repository)):
    auth_service = AuthService(user_repository)
    auth_data = auth_service.login(form_data.username, form_data.password)
    
    session_data = {
        "access_token": auth_data["access_token"],
        "user_id": auth_data["user_id"],
        "permissions": auth_data["permissions"],
    }

    response.set_cookie(
        key="session",
        value=json.dumps(session_data),
        httponly=False,
        secure=False,
        samesite="Lax",
        max_age=60 * 60 * 24,  # 1 dia
    )

    return ApiResponse(
        success=True,
        error=None,
        data={
            "user_id": auth_data["user_id"],
            "permissions": auth_data["permissions"]
        }
    )