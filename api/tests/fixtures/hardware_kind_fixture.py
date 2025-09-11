import pytest
from src.cruds.hardware_kind import HardwareKindRepository
from src.schemas.hardware_kind import HardwareKindBase

@pytest.fixture
def hardware_kind_repository(session) -> HardwareKindRepository:
    return HardwareKindRepository(session)

HARDWARE_KIND = HardwareKindBase(
    kind="Saída Digital",
)

@pytest.fixture
def create_hardware_kind(hardware_kind_repository: HardwareKindRepository, actor):
    def _create_hardware_kind(**overrides):
        hardware_kind_dict = HARDWARE_KIND.model_dump()
        hardware_kind_dict.update(overrides)
        hardware_kind = HardwareKindBase(**hardware_kind_dict)
        hardware_kind = hardware_kind_repository.save(hardware_kind.model_dump(), actor=actor)
        return hardware_kind
    return _create_hardware_kind
