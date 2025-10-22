from src.cruds.hardware_kind import HardwareKindRepository
from src.schemas.hardware_kind import HardwareKindBase

HARDWARE_KIND = HardwareKindBase(
    kind="Saída Digital",
)

def create_hardware_kind(session, actor=None, **overrides):
    repo = HardwareKindRepository(session)
    hardware_kind_dict = HARDWARE_KIND.model_dump()
    hardware_kind_dict.update(overrides)
    hardware_kind = HardwareKindBase(**hardware_kind_dict)
    hardware_kind = repo.save(hardware_kind.model_dump(), actor=actor)
    return hardware_kind
