# Reproducibility Notes

This repository keeps source data, processing scripts, and generated outputs together so the extraction can be rerun from a clean checkout.

## Default Run

```bash
uv sync
make reproduce
```

The default pipeline uses `--enrichment heuristic` to avoid depending on private credentials or remote API availability.

## Optional OpenAI Enrichment

To reproduce the OpenAI-assisted enrichment, create a local `.env` file from `.env.example` and set `OPENAI_API_KEY`.

```bash
uv run python scripts/02_extract_structured_food_data.py --enrichment openai
```

Do not commit `.env`.

