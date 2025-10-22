from src.cruds.installations import InstallationRepository
from src.schemas.installations import InstallationBase

INSTALLATION = InstallationBase(
    ip_address="192.168.0.1",
    name="Dispositivo de Conta",
    last_seen=None,
    is_online=False,
    device_id=1
)

def create_installation(session, actor=None, **overrides):
    repo = InstallationRepository(session)
    installation = INSTALLATION.model_dump()
    installation.update(overrides)
    installation = InstallationBase(**installation)
    installation = repo.save(installation.model_dump(), actor=actor)
    return installation
