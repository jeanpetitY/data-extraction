# WAFCT Data Extraction

This repository contains a reproducible pipeline for extracting structured food
composition data from the West African Food Composition Table files.

## Requirements

- Python 3.14
- uv

Install the locked environment:

```bash
uv sync
```

## Reproduce the Default Pipeline

The default reproducible run uses heuristic enrichment, so it does not require
an API key or network access to an external model provider.

```bash
make reproduce
```

This runs:

1. `scripts/01_export_excel_to_csv.py`
2. `scripts/02_extract_structured_food_data.py --enrichment heuristic`
3. `scripts/03_split_by_food_group.py`

## Optional OpenAI Enrichment

For OpenAI-assisted ingredient and geographical-area extraction:

```bash
cp .env.example .env
# edit .env and set OPENAI_API_KEY
uv run python scripts/02_extract_structured_food_data.py --enrichment openai
```

The heuristic mode should be used for reproducibility checks that must not
depend on private credentials or external API availability.

## Repository Structure

```text
.
├── data/                  # Source and generated data files
├── docs/                  # Pipeline and reproducibility notes
├── scripts/               # Reproducible command-line steps
├── src/data_extraction/   # Importable Python package
│   ├── enrichment/        # Heuristic and OpenAI metadata enrichment
│   ├── io/                # Excel and JSON input/output helpers
│   ├── parsing/           # WAFCT CSV parsing and component extraction
│   ├── resources/         # Static resources
│   ├── cli.py             # Command-line interface
│   ├── config.py          # Defaults and environment loading
│   └── pipeline.py        # End-to-end extraction orchestration
├── extract.py             # Backward-compatible CLI wrapper
├── main.py                # Excel-to-CSV wrapper
├── Makefile
├── pyproject.toml
└── uv.lock
```

## Useful Commands

```bash
make test
uv run python extract.py --enrichment heuristic --max-rows 10 --output /tmp/sample.json
uv run data-extraction --enrichment heuristic
```
