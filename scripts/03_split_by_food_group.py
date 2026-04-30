from pathlib import Path
import argparse
import json
import sys


sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from data_extraction.config import DEFAULT_OUTPUT_PATH
from data_extraction.io.json_writer import save_json_by_food_group


def main() -> None:
    """Split a structured JSON file into one JSON file per food group."""
    parser = argparse.ArgumentParser(description="Split structured JSON by food group.")
    parser.add_argument("--input", default=DEFAULT_OUTPUT_PATH)
    parser.add_argument("--output-dir", default="data/json/food_group")
    args = parser.parse_args()

    input_path = Path(args.input)
    data = json.loads(input_path.read_text(encoding="utf-8"))
    group_dir, group_count = save_json_by_food_group(
        data, output_path=args.input, grouped_dir=args.output_dir
    )
    print(f"Saved {group_count} food-group files in {group_dir}")


if __name__ == "__main__":
    main()
