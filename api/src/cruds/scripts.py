from datetime import date
from src.domain import exceptions as exc
from src.scripts.script_1 import script_1
from src.scripts.gerar_receitas import gerar_receitas

def exec_script(session, script_name: str, params: dict):
    if script_name == "script_1":
        data_text = params.get("data_base")
        considerar_fracao_liquida = params.get("considerar_fracao_liquida", False)
        data_base = date.fromisoformat(data_text) if data_text else date.today()
        return script_1(session, data_base=data_base, considerar_fracao_liquida=considerar_fracao_liquida)
    elif script_name == "gerar_receitas":
        data_text = params.get("data_base")
        data_base = date.fromisoformat(data_text) if data_text else date.today()
        receitas = gerar_receitas(session, data_base=data_base)
        return {"total": len(receitas), "receitas": [r.model_dump() for r in receitas]}
    else:
        raise exc.NotFound(f"Script {script_name} não encontrado.")
