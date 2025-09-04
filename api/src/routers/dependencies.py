from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from src.cruds.auth import AuthService
from src.cruds.users import UsersRepository
from src.core.db import get_session
from src.domain import exceptions as exc

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")

def get_current_user(token: str = Depends(oauth2_scheme), session = Depends(get_session)):
    user_service = UsersRepository(session)
    auth_service = AuthService(user_service)
    try:
        user_id = auth_service.verify_token(token)
        user = user_service.check_exists(user_id)
        return user
    except Exception as e:
        print(e)
        raise exc.Unauthorized("Token inválido")
