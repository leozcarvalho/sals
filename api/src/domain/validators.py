from src.domain import exceptions as exc

def validate_percent(value: float, field_name: str) -> float:
    if value <= 0 or value > 100:
        raise exc.InvalidData(f"O valor de {field_name} deve estar entre 0 e 100.")
    return value
