from typing import Any
import json
import os

from openai import OpenAI

from data_extraction.config import DEFAULT_MODEL, load_env
from data_extraction.enrichment.heuristics import enrich_with_heuristics


def enrich_with_openai(
    rows: list[dict[str, Any]], model: str = DEFAULT_MODEL, batch_size: int = 50
) -> dict[str, dict[str, Any]]:
    """Use OpenAI to enrich WAFCT rows with ingredients and geographical areas."""
    load_env()
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY manquante (.env ou variable d'environnement).")

    client = OpenAI(api_key=api_key)
    result: dict[str, dict[str, Any]] = {}

    for i in range(0, len(rows), batch_size):
        batch = rows[i : i + batch_size]
        payload = [
            {
                "code": r["code"],
                "food_name_english": r["food_name_english"],
                "food_name_french": r["food_name_french"],
            }
            for r in batch
        ]

        try:
            response = client.responses.create(
                model=model,
                instructions=(
                    "Extract ingredients and geographical area from food names. "
                    "geographical_area should be a single country name if explicitly present, else null. "
                    "Return only ingredients that can be inferred from names. "
                    "If no ingredient is inferable, return an empty list."
                ),
                input=json.dumps(payload, ensure_ascii=False),
                temperature=0,
                text={
                    "format": {
                        "type": "json_schema",
                        "name": "food_metadata_extraction",
                        "strict": True,
                        "schema": {
                            "type": "object",
                            "properties": {
                                "items": {
                                    "type": "array",
                                    "items": {
                                        "type": "object",
                                        "properties": {
                                            "code": {"type": "string"},
                                            "ingredients": {
                                                "type": "array",
                                                "items": {"type": "string"},
                                            },
                                            "geographical_area": {
                                                "type": ["string", "null"]
                                            },
                                        },
                                        "required": [
                                            "code",
                                            "ingredients",
                                            "geographical_area",
                                        ],
                                        "additionalProperties": False,
                                    },
                                }
                            },
                            "required": ["items"],
                            "additionalProperties": False,
                        },
                    }
                },
            )

            parsed = json.loads(response.output_text)
            for item in parsed.get("items", []):
                code = item.get("code")
                if code:
                    result[code] = {
                        "ingredients": item.get("ingredients", []),
                        "geographical_area": item.get("geographical_area"),
                    }
        except Exception:
            result.update(enrich_with_heuristics(batch))

    return result
