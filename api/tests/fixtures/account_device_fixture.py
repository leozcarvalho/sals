import pytest
from src.cruds.installations import InstallationRepository
from src.schemas.installations import InstallationBase

@pytest.fixture
def installation_repository(session) -> InstallationRepository:
    return InstallationRepository(session)

INSTALLATION = InstallationBase(
    ip_address="192.168.0.1",
    name="Dispositivo de Conta",
    last_seen=None,
    is_online=False,
    device_id=1
)

@pytest.fixture()
def create_installation(installation_repository: InstallationRepository, actor):
    def create_installation(**overrides):
        installation = INSTALLATION.model_dump()
        installation.update(overrides)
        installation = InstallationBase(**installation)
        installation = installation_repository.save(installation.model_dump(), actor=actor)
        return installation
    return create_installation
