import hashlib

from sqlalchemy.orm import Session
from src.domain import User
from src.cruds.repo import Repository


class UsersRepository(Repository):
    def __init__(self, db: Session):
        super().__init__(User, db)

    def __get_encrypted_password(self, password):
        return hashlib.sha256(password.encode()).hexdigest()

    def save(self, values, actor=None):
        if 'password' in values:
            values['password'] = self.__get_encrypted_password(values.pop('password'))
        return super().save(values, actor)

    def update(self, id, values, actor=None):
        if 'password' in values:
            values['password'] = self.__get_encrypted_password(values.pop('password'))
        return super().update(id, values, actor)
    
