import pytest
from src.cruds.instalations import InstalationRepository
from src.schemas.instalations import InstalationBase

@pytest.fixture
def instalation_repository(session) -> InstalationRepository:
    return InstalationRepository(session)

INSTALATION = InstalationBase(
    ip_address="192.168.0.1",
    name="Dispositivo de Conta",
    last_seen=None,
    is_online=False,
    device_id=1
)

@pytest.fixture()
def create_instalation(instalation_repository: InstalationRepository, actor):
    def create_instalation(**overrides):
        instalation_dict = INSTALATION.model_dump()
        instalation_dict.update(overrides)
        instalation = InstalationBase(**instalation_dict)
        instalation = instalation_repository.save(instalation.model_dump(), actor=actor)
        return instalation
    return create_instalation
