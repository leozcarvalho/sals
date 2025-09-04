import hashlib

from sqlalchemy.orm import Session
from src.domain import Profile
from src.cruds.repo import Repository
from src.domain import permissions

class ProfileRepository(Repository):
    def __init__(self, session: Session):
        super().__init__(Profile, session)

    def get_permissions(self):
        return [{"value": perm.value, "label": perm.label} for perm in permissions.PermissionEnum]
