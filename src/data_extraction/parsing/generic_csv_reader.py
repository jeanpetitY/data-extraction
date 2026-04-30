from typing import Any
import re

import pandas as pd


def read_generic_csv_rows(
    csv_path: str,
    prop_names: list[str],
    max_rows: int | None = None,
) -> list[dict[str, Any]]:
    """Read CSV rows and map template property names to matching CSV columns."""
    df = pd.read_csv(csv_path, dtype=str, keep_default_na=False)

    if max_rows is not None:
        df = df.head(max_rows)

    column_by_prop_name = map_columns_to_prop_names(df.columns, prop_names)
    rows: list[dict[str, Any]] = []

    for index, row in df.iterrows():
        values: dict[str, Any] = {}
        source_row = {str(column): normalize_cell(row[column]) for column in df.columns}

        for prop_name in prop_names:
            column = column_by_prop_name.get(prop_name)
            values[prop_name] = normalize_cell(row[column]) if column else None

        rows.append(
            {
                "row_id": str(index),
                "values": values,
                "source_row": source_row,
            }
        )

    return rows


def map_columns_to_prop_names(columns: Any, prop_names: list[str]) -> dict[str, str]:
    """Map requested property names to CSV columns using normalized names."""
    normalized_columns = {normalize_name(column): str(column) for column in columns}
    mapping: dict[str, str] = {}

    for prop_name in prop_names:
        column = normalized_columns.get(normalize_name(prop_name))
        if column:
            mapping[prop_name] = column

    return mapping


def normalize_name(value: str) -> str:
    """Normalize a column or property name for loose name matching."""
    return re.sub(r"[^a-z0-9]+", "_", str(value).strip().lower()).strip("_")


def normalize_cell(value: Any) -> str | None:
    """Normalize an input cell to a string value or None for empty cells."""
    text = str(value).strip()
    if not text or text.lower() == "nan":
        return None
    return text
