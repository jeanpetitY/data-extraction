from data_extraction.enrichment.heuristics import heuristic_extract_geographical_area
from data_extraction.io.json_writer import slugify_filename
from data_extraction.parsing.components import (
    is_component_column,
    normalize_component_value,
    split_name_and_unit,
)
from data_extraction.parsing.food_codes import is_food_code
from data_extraction.pipeline import resolve_geographical_area


def test_is_food_code() -> None:
    """Validate WAFCT food code pattern detection."""
    assert is_food_code("01_172")
    assert not is_food_code("Cereals and their products")


def test_split_name_and_unit() -> None:
    """Validate component column parsing into name and unit."""
    assert split_name_and_unit("Energy (kJ)") == ("Energy", "kJ")
    assert split_name_and_unit("Food name") == ("Food name", None)


def test_normalize_component_value() -> None:
    """Validate empty and non-empty component value normalization."""
    assert normalize_component_value(" 12.3 ") == "12.3"
    assert normalize_component_value("") is None
    assert normalize_component_value("nan") is None


def test_is_component_column_excludes_edible_portion_coefficient() -> None:
    """Validate that edible portion metadata is excluded from components."""
    assert not is_component_column(
        "Edible portion coefficient 1 (from as purchased to as described)"
    )
    assert is_component_column("Energy\n(kJ)")


def test_heuristic_extract_geographical_area() -> None:
    """Validate heuristic geographical area extraction."""
    assert heuristic_extract_geographical_area("Millet porridge, Senegal") == "Senegal"
    assert heuristic_extract_geographical_area("Millet porridge") is None


def test_slugify_filename() -> None:
    """Validate food group names are converted into safe filenames."""
    assert (
        slugify_filename("Cereals and their products / Céréales")
        == "cereals_and_their_products_-_crales"
    )


def test_resolve_geographical_area_defaults_to_west_africa() -> None:
    """Validate geographical area fallback behavior."""
    assert resolve_geographical_area({}, "01_001") == "West Africa"
    assert (
        resolve_geographical_area(
            {"01_001": {"geographical_area": "Senegal"}},
            "01_001",
        )
        == "Senegal"
    )
