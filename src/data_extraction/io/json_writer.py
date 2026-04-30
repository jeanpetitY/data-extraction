from typing import Any
from pathlib import Path
import json
import re


def save_json(data: list[dict[str, Any]], output_path: str) -> None:
    out = Path(output_path)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def slugify_filename(text: str) -> str:
    normalized = text.strip().lower()
    normalized = normalized.replace("/", " - ")
    normalized = re.sub(r"\s+", "_", normalized)
    normalized = re.sub(r"[^a-z0-9_\\-]", "", normalized)
    normalized = re.sub(r"_+", "_", normalized).strip("_")
    return normalized or "unknown_group"


def save_json_by_food_group(
    data: list[dict[str, Any]],
    output_path: str,
    grouped_dir: str | None = None,
) -> tuple[str, int]:
    out = Path(output_path)
    base_dir = Path(grouped_dir) if grouped_dir else out.parent / f"{out.stem}_by_group"
    base_dir.mkdir(parents=True, exist_ok=True)

    grouped: dict[str, list[dict[str, Any]]] = {}
    for item in data:
        group = item.get("food_group") or "Uncategorized"
        grouped.setdefault(str(group), []).append(item)

    for group_name, items in grouped.items():
        filename = f"{slugify_filename(group_name)}.json"
        (base_dir / filename).write_text(
            json.dumps(items, ensure_ascii=False, indent=2), encoding="utf-8"
        )

    return str(base_dir), len(grouped)

