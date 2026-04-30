from typing import Any
import csv

import pandas as pd

from data_extraction.parsing.components import (
    is_component_column,
    normalize_component_value,
    split_name_and_unit,
)
from data_extraction.parsing.food_codes import is_food_code


def extract_food_group_mapping(csv_path: str) -> dict[str, str | None]:
    """
    Build a mapping from food code (e.g. 01_172) to section title
    (e.g. Cereals and their products/...).
    """
    code_to_group: dict[str, str | None] = {}
    current_group: str | None = None

    with open(csv_path, newline="", encoding="utf-8-sig") as file:
        reader = csv.reader(file)
        rows = list(reader)

    for row in rows[3:]:
        if not row:
            continue

        code_or_section = (row[0] if len(row) > 0 else "").strip()
        en_name = (row[1] if len(row) > 1 else "").strip()
        fr_name = (row[2] if len(row) > 2 else "").strip()

        if code_or_section and not is_food_code(code_or_section) and not en_name and not fr_name:
            current_group = code_or_section
            continue

        if is_food_code(code_or_section):
            code_to_group[code_or_section] = current_group

    return code_to_group


def read_food_rows_with_pandas(
    csv_path: str, max_rows: int | None = None
) -> list[dict[str, Any]]:
    df = pd.read_csv(csv_path, dtype=str, keep_default_na=False)
    code_to_group = extract_food_group_mapping(csv_path)

    code_col = "Code"
    en_col = "Food name in English"
    fr_col = "Food name in French"
    scientific_col = "Scientific name"

    missing = [c for c in (code_col, en_col, fr_col, scientific_col) if c not in df.columns]
    if missing:
        raise ValueError(f"Colonnes manquantes dans le CSV: {missing}")

    df = df[df[code_col].apply(is_food_code)].copy()

    if max_rows is not None:
        df = df.head(max_rows)

    component_columns = [col for col in df.columns[5:] if is_component_column(col)]
    rows: list[dict[str, Any]] = []

    for _, row in df.iterrows():
        components: list[dict[str, Any]] = []

        for col in component_columns:
            value = normalize_component_value(row[col])
            if value is None:
                continue

            name, unit = split_name_and_unit(col)
            components.append(
                {
                    "name": name,
                    "value": value,
                    "unit": unit,
                }
            )

        rows.append(
            {
                "code": str(row[code_col]).strip(),
                "food_name_english": str(row[en_col]).strip(),
                "food_name_french": str(row[fr_col]).strip(),
                "scientific_name": str(row[scientific_col]).strip(),
                "food_group": code_to_group.get(str(row[code_col]).strip()),
                "components": components,
            }
        )

    return rows
