import json
from fastapi import Cookie, Depends
from src.cruds.users import UsersRepository
from src.cruds.auth import AuthService
from src.domain import exceptions as exc
from src.core.db import get_session

def get_current_user(
    session_cookie: str = Cookie(None, alias="session"),
    session=Depends(get_session),
):
    """
    Lê o cookie 'session', valida o token e retorna o usuário autenticado.
    """
    if not session_cookie:
        raise exc.Unauthorized("Não autenticado")

    try:
        # 🔹 Decodifica o JSON do cookie
        data = json.loads(session_cookie)
        token = data.get("access_token")
        if not token:
            raise exc.Unauthorized("Token ausente")

        # 🔹 Valida o token
        user_service = UsersRepository(session)
        auth_service = AuthService(user_service)
        user_id = auth_service.verify_token(token)

        # 🔹 Busca usuário
        user = user_service.check_exists(user_id)
        return user
    except Exception as e:
        print(f"Erro ao validar usuário: {e}")
        raise exc.Unauthorized("Sessão inválida")
