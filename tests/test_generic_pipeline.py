import json

from data_extraction.enrichment.generic_openai_enrichment import (
    build_dynamic_extraction_prompt,
    build_dynamic_schema,
)
from data_extraction.generic_pipeline import build_generic_list
from data_extraction.template import load_template_prop_names


def test_load_csv_template_prop_names(tmp_path) -> None:
    """Validate prop_name loading from CSV templates."""
    template = tmp_path / "template.csv"
    template.write_text(
        "prop_id,prop_name\nP001,food_name\nP002,geographical_area\n",
        encoding="utf-8",
    )

    assert load_template_prop_names(template) == ["food_name", "geographical_area"]


def test_load_json_template_prop_names(tmp_path) -> None:
    """Validate prop_name loading from JSON templates."""
    template = tmp_path / "template.json"
    template.write_text(
        json.dumps(
            [
                {"prop_id": "P001", "prop_name": "food_name"},
                {"prop_id": "P002", "prop_name": "geographical_area"},
            ]
        ),
        encoding="utf-8",
    )

    assert load_template_prop_names(template) == ["food_name", "geographical_area"]


def test_build_generic_list_from_template_and_csv(tmp_path) -> None:
    """Validate generic extraction from a template and matching CSV columns."""
    template = tmp_path / "template.csv"
    template.write_text(
        "prop_id,prop_name\nP001,food_name\nP002,geographical_area\nP003,missing_prop\n",
        encoding="utf-8",
    )
    data = tmp_path / "data.csv"
    data.write_text(
        "food_name,geographical_area,ignored\nMillet porridge,West Africa,x\n",
        encoding="utf-8",
    )

    assert build_generic_list(str(data), str(template)) == [
        {
            "food_name": "Millet porridge",
            "geographical_area": "West Africa",
            "missing_prop": None,
        }
    ]


def test_build_dynamic_prompt_uses_template_props() -> None:
    """Validate dynamic prompts include template property names."""
    prompt = build_dynamic_extraction_prompt(["food_name", "geographical_area"])

    assert "food_name" in prompt
    assert "geographical_area" in prompt


def test_build_dynamic_schema_uses_template_props() -> None:
    """Validate dynamic schemas require template property names."""
    schema = build_dynamic_schema(["food_name", "geographical_area"])
    values = schema["properties"]["items"]["items"]["properties"]["values"]

    assert values["required"] == ["food_name", "geographical_area"]
    assert "food_name" in values["properties"]
    assert "geographical_area" in values["properties"]
