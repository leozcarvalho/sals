from src.domain import exceptions as exc
from src.scripts.script_1 import script_1

def exec_script(session, script_name: str, params: dict):
    if script_name == "script_1":
        return script_1(session, **params)
    else:
        raise exc.NotFound(f"Script {script_name} not found.")
