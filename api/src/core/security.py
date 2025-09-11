from datetime import datetime, timedelta, timezone
from typing import Optional
from jose import JWTError, jwt
import hashlib
import hmac

from src.domain import exceptions as exc
from src.core.config import settings


class Security:
    def __init__(self):
        self.secret_key = settings.SECRET_KEY
        self.algorithm = settings.ALGORITHM
        self.access_token_expire_minutes = settings.ACCESS_TOKEN_EXPIRE_MINUTES

    # -------------------- SENHAS -------------------- #
    def hash_password(self, password: str) -> str:
        """
        Gera hash seguro para a senha usando SHA-256.
        """
        return hashlib.sha256(password.encode("utf-8")).hexdigest()

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """
        Verifica se a senha informada confere com o hash.
        """
        calculated_hash = hashlib.sha256(plain_password.encode("utf-8")).hexdigest()
        return hmac.compare_digest(calculated_hash, hashed_password)

    # -------------------- JWT -------------------- #
    def create_access_token(
        self,
        data: dict,
        expires_delta: Optional[timedelta] = None
    ) -> str:
        """
        Gera token JWT.
        """
        to_encode = data.copy()
        expire = datetime.now(timezone.utc) + (expires_delta or timedelta(minutes=self.access_token_expire_minutes))
        to_encode.update({"exp": expire})
        return jwt.encode(to_encode, self.secret_key, algorithm=self.algorithm)

    def decode_access_token(self, token: str) -> dict:
        """
        Decodifica e valida o token JWT.
        """
        try:
            return jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
        except JWTError:
            raise exc.Unauthorized("Token inválido ou expirado")
