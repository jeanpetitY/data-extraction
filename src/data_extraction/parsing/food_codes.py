import re

def is_food_code(value: str) -> bool:
    return bool(re.match(r"^\d{2}_\d+", str(value).strip()))

