import re

def is_food_code(value: str) -> bool:
    """Return whether a value matches the WAFCT food code pattern."""
    return bool(re.match(r"^\d{2}_\d+", str(value).strip()))
