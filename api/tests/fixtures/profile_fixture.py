from src.cruds.profile import ProfileRepository
from src.domain.profile import Profile
from src.domain.permissions import PermissionEnum
from src.schemas.profile import ProfileCreate, ProfileUpdate


PROFILE = ProfileCreate(
    name="Administrador",
    permissions=[p.value for p in PermissionEnum],
)

def create_profile(session, actor=None, **overrides):
    repo = ProfileRepository(session)
    data = PROFILE.model_dump()
    data.update(overrides)
    profile = repo.save(data, actor=actor)
    return profile
