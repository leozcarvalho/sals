import pytest
from src.cruds.profile import ProfileRepository
from src.domain.profile import Profile

@pytest.fixture
def profile_repository(session):
    repo = ProfileRepository(session)
    return repo

@pytest.fixture
def create_profile(session, profile_repository):
    def _create_profile(**overrides):
        profile_data = {
            "name": "Test Profile",
            "permissions": {"read": True, "write": False}
        }
        profile_data.update(overrides)
        profile = Profile(**profile_data)
        profile = profile_repository.create(profile)
        return profile

    return _create_profile