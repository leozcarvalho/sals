from sqlalchemy.orm import Session
from src.domain import User
from src.cruds.repo import Repository
from src.core.security import Security


class UsersRepository(Repository):
    def __init__(self, db: Session):
        super().__init__(User, db)
        self.security = Security()

    def save(self, values, actor=None):
        if 'password' in values:
            values['password'] = self.security.hash_password(values.pop('password'))
        return super().save(values, actor)

    def update(self, id, values, actor=None):
        if 'password' in values:
            values['password'] = self.security.hash_password(values.pop('password'))
        return super().update(id, values, actor)
    
