from typing import Any, Literal

from data_extraction.config import DEFAULT_MODEL
from data_extraction.enrichment.generic_openai_enrichment import (
    enrich_missing_props_with_openai,
)
from data_extraction.parsing.generic_csv_reader import read_generic_csv_rows
from data_extraction.template import load_template_prop_names


GenericEnrichmentMode = Literal["none", "openai"]


def build_generic_list(
    csv_path: str,
    template_path: str,
    model: str = DEFAULT_MODEL,
    batch_size: int = 50,
    max_rows: int | None = None,
    enrichment: GenericEnrichmentMode = "none",
) -> list[dict[str, Any]]:
    """Build generic JSON records from a data CSV and a property template."""
    prop_names = load_template_prop_names(template_path)
    rows = read_generic_csv_rows(csv_path, prop_names, max_rows=max_rows)

    if enrichment == "none":
        return [row["values"] for row in rows]

    if enrichment == "openai":
        return enrich_missing_props_with_openai(
            rows,
            prop_names,
            model=model,
            batch_size=batch_size,
        )

    raise ValueError(f"Mode d'enrichissement generique non supporte: {enrichment}")
