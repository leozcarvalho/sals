from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from src.cruds.auth import AuthService
from src.schemas.auth import LoginResponse
from src.cruds.users import UsersRepository
from src.core.db import get_session

auth_router = APIRouter(tags=["Auth"])

def get_user_repository(session = Depends(get_session)):
    return UsersRepository(session)

@auth_router.post("/login", response_model=LoginResponse)
def login(form_data: OAuth2PasswordRequestForm = Depends(), user_repository: UsersRepository = Depends(get_user_repository)):
    auth_service = AuthService(user_repository)
    return auth_service.login(form_data.username, form_data.password)
