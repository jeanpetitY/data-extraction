import argparse

from data_extraction.config import DEFAULT_CSV_PATH, DEFAULT_MODEL, DEFAULT_OUTPUT_PATH
from data_extraction.io.json_writer import save_json, save_json_by_food_group
from data_extraction.pipeline import build_final_list


def main() -> None:
    parser = argparse.ArgumentParser(
        description=(
            "CSV -> list[dict] with keys: portion, code, food_name_english, "
            "food_name_french, scientific_name, food_group, geographical_area, "
            "components, ingredients"
        )
    )
    parser.add_argument("--csv", default=DEFAULT_CSV_PATH)
    parser.add_argument("--output", default=DEFAULT_OUTPUT_PATH)
    parser.add_argument("--model", default=DEFAULT_MODEL)
    parser.add_argument("--batch-size", type=int, default=50)
    parser.add_argument("--max-rows", type=int, default=None)
    parser.add_argument(
        "--enrichment",
        choices=["openai", "heuristic"],
        default="openai",
        help="Use 'heuristic' to run without external API access.",
    )
    parser.add_argument(
        "--split-by-food-group",
        action="store_true",
        help="If set, also save one JSON file per food_group.",
    )
    parser.add_argument(
        "--group-output-dir",
        default=None,
        help=(
            "Optional output directory for per-group files. "
            "Default: <output_stem>_by_group next to --output."
        ),
    )
    args = parser.parse_args()

    final_data = build_final_list(
        csv_path=args.csv,
        model=args.model,
        batch_size=args.batch_size,
        max_rows=args.max_rows,
        enrichment=args.enrichment,
    )
    save_json(final_data, args.output)
    print(f"Saved {len(final_data)} items to {args.output}")

    if args.split_by_food_group:
        group_dir, group_count = save_json_by_food_group(
            final_data, output_path=args.output, grouped_dir=args.group_output_dir
        )
        print(f"Saved {group_count} food-group files in {group_dir}")

