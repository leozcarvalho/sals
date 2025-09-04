import pytest
from src.cruds.hardware_connection_template import HardwareConnectionTemplateRepository
from src.schemas.hardware_connection_template import HardwareConnectionTemplateBase

@pytest.fixture
def hardware_connection_template_repository(session) -> HardwareConnectionTemplateRepository:
    return HardwareConnectionTemplateRepository(session)

HARDWARE_CONNECTION_TEMPLATE = HardwareConnectionTemplateBase(
        name="Template de Conexão",
        template_url="http://{ip}/get",
    )

@pytest.fixture()
def create_hardware_connection_template(hardware_connection_template_repository: HardwareConnectionTemplateRepository, actor):
    def _create_hardware_connection_template(**overrides):
        hardware_connection_template_dict = HARDWARE_CONNECTION_TEMPLATE.model_dump()
        hardware_connection_template_dict.update(overrides)
        hardware_connection_template = HardwareConnectionTemplateBase(**hardware_connection_template_dict)
        hardware_connection_template = hardware_connection_template_repository.save(hardware_connection_template.model_dump(), actor=actor)
        return hardware_connection_template
    return _create_hardware_connection_template
