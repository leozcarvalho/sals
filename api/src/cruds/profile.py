import hashlib

from sqlalchemy.orm import Session
from src.domain import Profile
from src.cruds.repo import Repository

class ProfileRepository(Repository):
    def __init__(self, session: Session):
        super().__init__(Profile, session)
