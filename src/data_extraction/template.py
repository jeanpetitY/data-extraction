from pathlib import Path
from typing import Any
import csv
import json


def load_template_prop_names(template_path: str | Path) -> list[str]:
    """Load property names from a CSV or JSON template file."""
    path = Path(template_path)
    suffix = path.suffix.lower()

    if suffix == ".csv":
        return load_csv_template_prop_names(path)
    if suffix == ".json":
        return load_json_template_prop_names(path)

    raise ValueError(f"Format de template non supporte: {path.suffix}")


def load_csv_template_prop_names(template_path: Path) -> list[str]:
    """Load unique non-empty prop_name values from a CSV template."""
    with template_path.open(newline="", encoding="utf-8-sig") as file:
        reader = csv.DictReader(file)
        if "prop_name" not in (reader.fieldnames or []):
            raise ValueError("Le template CSV doit contenir une colonne 'prop_name'.")
        return unique_non_empty(row["prop_name"] for row in reader)


def load_json_template_prop_names(template_path: Path) -> list[str]:
    """Load unique non-empty prop_name values from a JSON template."""
    data = json.loads(template_path.read_text(encoding="utf-8"))
    return unique_non_empty(extract_prop_names(data))


def extract_prop_names(value: Any) -> list[str]:
    """Recursively extract prop_name values from nested JSON-like data."""
    if isinstance(value, dict):
        names: list[str] = []
        if "prop_name" in value:
            names.append(str(value["prop_name"]))
        for child in value.values():
            names.extend(extract_prop_names(child))
        return names

    if isinstance(value, list):
        names = []
        for item in value:
            names.extend(extract_prop_names(item))
        return names

    return []


def unique_non_empty(values: Any) -> list[str]:
    """Return unique non-empty string values while preserving input order."""
    seen: set[str] = set()
    result: list[str] = []

    for value in values:
        text = str(value).strip()
        if not text or text in seen:
            continue
        seen.add(text)
        result.append(text)

    return result
