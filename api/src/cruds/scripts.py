from datetime import date
from src.domain import exceptions as exc
from src.scripts.script_1 import script_1

def exec_script(session, script_name: str, params: dict):
    if script_name == "script_1":
        data_text = params.get("data_base")
        ignorar_fracao_liquida = params.get("ignorar_fracao_liquida", False)
        data_base = date.fromisoformat(data_text) if data_text else date.today()
        return script_1(session, data_base=data_base, ignorar_fracao_liquida=ignorar_fracao_liquida)
    else:
        raise exc.NotFound(f"Script {script_name} não encontrado.")
