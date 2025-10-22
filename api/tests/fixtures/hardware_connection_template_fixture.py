from src.cruds.hardware_connection_template import HardwareConnectionTemplateRepository
from src.schemas.hardware_connection_template import HardwareConnectionTemplateBase

HARDWARE_CONNECTION_TEMPLATE = HardwareConnectionTemplateBase(
        name="Template de Conexão",
        template_url="http://{ip}/get",
        query_string="?valvula1={valor}&valvula2={valor2}"
    )

def create_hardware_connection_template(session, actor=None, **overrides):
    repo = HardwareConnectionTemplateRepository(session)
    hardware_connection_template_dict = HARDWARE_CONNECTION_TEMPLATE.model_dump()
    hardware_connection_template_dict.update(overrides)
    hardware_connection_template = HardwareConnectionTemplateBase(**hardware_connection_template_dict)
    hardware_connection_template = repo.save(hardware_connection_template.model_dump(), actor=actor)
    return hardware_connection_template
