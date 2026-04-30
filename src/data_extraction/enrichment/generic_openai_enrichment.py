from typing import Any
import json
import os

from openai import OpenAI

from data_extraction.config import DEFAULT_MODEL, load_env


def enrich_missing_props_with_openai(
    rows: list[dict[str, Any]],
    prop_names: list[str],
    model: str = DEFAULT_MODEL,
    batch_size: int = 50,
) -> list[dict[str, Any]]:
    """Use OpenAI to fill missing template properties from generic CSV rows."""
    load_env()
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY manquante (.env ou variable d'environnement).")

    client = OpenAI(api_key=api_key)
    enriched_rows = [dict(row["values"]) for row in rows]

    for i in range(0, len(rows), batch_size):
        batch = rows[i : i + batch_size]
        payload = [
            {
                "row_id": row["row_id"],
                "existing_values": row["values"],
                "source_row": row["source_row"],
            }
            for row in batch
        ]

        response = client.responses.create(
            model=model,
            instructions=build_dynamic_extraction_prompt(prop_names),
            input=json.dumps(payload, ensure_ascii=False),
            temperature=0,
            text={
                "format": {
                    "type": "json_schema",
                    "name": "generic_property_extraction",
                    "strict": True,
                    "schema": build_dynamic_schema(prop_names),
                }
            },
        )

        parsed = json.loads(response.output_text)
        values_by_row_id = {
            str(item["row_id"]): item["values"] for item in parsed.get("items", [])
        }

        for offset, row in enumerate(batch):
            extracted = values_by_row_id.get(row["row_id"], {})
            for prop_name in prop_names:
                if enriched_rows[i + offset].get(prop_name) is None:
                    enriched_rows[i + offset][prop_name] = extracted.get(prop_name)

    return enriched_rows


def build_dynamic_extraction_prompt(prop_names: list[str]) -> str:
    """Build an extraction prompt from user-provided template properties."""
    props = ", ".join(prop_names)
    return (
        "Extract the requested properties from each CSV row. "
        "Use only information explicitly present in source_row or clearly inferable from it. "
        "Keep existing_values unchanged when already provided. "
        "Return null when a property cannot be found or inferred. "
        f"The requested property names are: {props}."
    )


def build_dynamic_schema(prop_names: list[str]) -> dict[str, Any]:
    """Build a strict JSON schema for dynamic property extraction."""
    value_schema = {"type": ["string", "null"]}
    return {
        "type": "object",
        "properties": {
            "items": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "row_id": {"type": "string"},
                        "values": {
                            "type": "object",
                            "properties": {
                                prop_name: value_schema for prop_name in prop_names
                            },
                            "required": prop_names,
                            "additionalProperties": False,
                        },
                    },
                    "required": ["row_id", "values"],
                    "additionalProperties": False,
                },
            }
        },
        "required": ["items"],
        "additionalProperties": False,
    }
