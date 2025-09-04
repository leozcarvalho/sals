import pytest
from src.services.profile_service import ProfileService
from src.repositories.profile_repository import ProfileRepository
from src.domain.profile import Profile

@pytest.fixture()
def profile_service(session):
    repo = ProfileRepository(session)
    service = ProfileService(repo)
    return service

@pytest.fixture()
def create_profile(session, profile_service):
    async def _create_profile(**overrides):
        profile_data = {
            "name": "Test Profile",
            "permissions": {"read": True, "write": False}
        }
        profile_data.update(overrides)

        profile = Profile(**profile_data)
        profile = profile_service.create(profile)
        return profile

    return _create_profile