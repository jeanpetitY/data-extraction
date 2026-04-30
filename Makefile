.PHONY: reproduce export extract split test

reproduce: export extract split

export:
	uv run python scripts/01_export_excel_to_csv.py

extract:
	uv run python scripts/02_extract_structured_food_data.py --enrichment heuristic

split:
	uv run python scripts/03_split_by_food_group.py

test:
	uv run python -m compileall extract.py main.py scripts src
	uv run pytest
