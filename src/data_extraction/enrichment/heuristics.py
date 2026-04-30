import re

from data_extraction.resources.african_countries import AFRICAN_COUNTRIES


def heuristic_extract_ingredients(english_name: str) -> list[str]:
    """Infer simple ingredient candidates from an English food name."""
    tail = english_name.split(":", 1)[1] if ":" in english_name else english_name
    tail = re.sub(r"\*", "", tail)
    return [
        p.strip()
        for p in re.split(r",| and | with ", tail, flags=re.IGNORECASE)
        if p.strip()
    ]


def heuristic_extract_geographical_area(text: str) -> str | None:
    """Return the first African country explicitly mentioned in text."""
    for country in AFRICAN_COUNTRIES:
        pattern = rf"\b{re.escape(country)}\b"
        if re.search(pattern, text, flags=re.IGNORECASE):
            return country
    return None


def enrich_with_heuristics(rows: list[dict]) -> dict[str, dict]:
    """Enrich WAFCT rows with heuristic ingredients and geographical areas."""
    result: dict[str, dict] = {}
    for row in rows:
        text = f"{row['food_name_english']} {row['food_name_french']}"
        result[row["code"]] = {
            "ingredients": heuristic_extract_ingredients(row["food_name_english"]),
            "geographical_area": heuristic_extract_geographical_area(text),
        }
    return result
