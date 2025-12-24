from src.domain.exceptions import InvalidData

def range_validator(value, min_value=None, max_value=None):
    if min_value is not None and value < min_value:
        raise InvalidData(f"{value} deve ser maior ou igual a {min_value}")
    if max_value is not None and value > max_value:
        raise InvalidData(f"{value} deve ser menor ou igual a {max_value}")
    return value
