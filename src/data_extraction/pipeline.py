from typing import Any, Literal

from data_extraction.config import DEFAULT_GEOGRAPHICAL_AREA, DEFAULT_MODEL
from data_extraction.enrichment.heuristics import enrich_with_heuristics
from data_extraction.enrichment.openai_enrichment import enrich_with_openai
from data_extraction.parsing.wafct_reader import read_food_rows_with_pandas


EnrichmentMode = Literal["openai", "heuristic"]


def resolve_geographical_area(
    enriched_by_code: dict[str, dict[str, Any]], code: str
) -> str:
    """Return an enriched geographical area or the dataset default area."""
    return (
        enriched_by_code.get(code, {}).get("geographical_area")
        or DEFAULT_GEOGRAPHICAL_AREA
    )


def build_final_list(
    csv_path: str,
    model: str = DEFAULT_MODEL,
    batch_size: int = 50,
    max_rows: int | None = None,
    enrichment: EnrichmentMode = "openai",
) -> list[dict[str, Any]]:
    """Build the WAFCT-specific structured JSON records from a source CSV."""
    rows = read_food_rows_with_pandas(csv_path, max_rows=max_rows)

    if enrichment == "heuristic":
        enriched_by_code = enrich_with_heuristics(rows)
    elif enrichment == "openai":
        enriched_by_code = enrich_with_openai(rows, model=model, batch_size=batch_size)
    else:
        raise ValueError(f"Mode d'enrichissement non supporte: {enrichment}")

    return [
        {
            "portion": "100g",
            "code": row["code"],
            "food_name_english": row["food_name_english"],
            "food_name_french": row["food_name_french"],
            "scientific_name": row["scientific_name"],
            "food_group": row["food_group"],
            "geographical_area": resolve_geographical_area(enriched_by_code, row["code"]),
            "components": row["components"],
            "ingredients": enriched_by_code.get(row["code"], {}).get("ingredients", []),
        }
        for row in rows
    ]
