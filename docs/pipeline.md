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

## Generic Template Mode

For non-WAFCT datasets, provide a CSV data file and a template file:

```bash
uv run data-extraction \
  --csv path/to/data.csv \
  --template templates/example_template.csv \
  --output path/to/output.json \
  --generic-enrichment none
```

The template may be CSV or JSON. The only field required by the generic
pipeline is `prop_name`; `prop_id` can be chosen freely by the user.

If `--generic-enrichment openai` is used, the prompt and JSON schema are built
dynamically from the template `prop_name` values. Existing CSV column values are
kept, and missing values are inferred by the model when possible.
