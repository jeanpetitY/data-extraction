from typing import Any
import re


def split_name_and_unit(column_name: str) -> tuple[str, str | None]:
    """Split a component column label into a display name and optional unit."""
    label = re.sub(r"\s+", " ", str(column_name).replace("\n", " ")).strip()
    match = re.search(r"\(([^()]*)\)\s*$", label)
    if not match:
        return label, None
    unit = match.group(1).strip()
    name = label[: match.start()].strip(" ;")
    return name, unit


def normalize_component_value(raw: Any) -> str | None:
    """Normalize a raw component value to a string or None when it is empty."""
    if raw is None:
        return None
    text = str(raw).strip()
    if text == "" or text.lower() == "nan":
        return None
    return text


def is_component_column(column_name: str) -> bool:
    """Return whether a source column should be exported as a nutrient component."""
    name, _ = split_name_and_unit(column_name)
    normalized = re.sub(r"\s+", " ", name).strip().lower()
    return not normalized.startswith("edible portion coefficient")
