# Pipeline

The extraction workflow is split into three reproducible steps:

1. Export the Excel workbook sheets to CSV files.
2. Parse the WAFCT CSV table and enrich food names with ingredients and geographical area.
3. Split the structured JSON output by food group.

The default reproducible command uses heuristic enrichment, so it does not require an external API key:

```bash
make reproduce
```

OpenAI enrichment remains available for experiments that explicitly need it:

```bash
uv run python scripts/02_extract_structured_food_data.py --enrichment openai
```

