from src.cruds.users import UsersRepository
from src.core.security import Security
from src.domain import exceptions as exc

class AuthService:
    def __init__(self, user_service: UsersRepository):
        self.user_service = user_service
        self.security = Security()

    def authenticate(self, email: str, password: str):
        user = self.user_service.get_one(filters={"email": email})
        if not user or not self.security.verify_password(password, user.password):
            raise exc.Unauthorized("Email ou senha inválidos")
        return user

    def login(self, email: str, password: str):
        user = self.authenticate(email, password)
        token = self.security.create_access_token(data={
            "sub": str(user.id),
        })
        return {"access_token": token, "token_type": "bearer"}

    def verify_token(self, token: str):
        payload = self.security.decode_access_token(token)
        user_id = payload.get("sub")
        if user_id is None:
            raise exc.Unauthorized("Token inválido")
        return int(user_id)