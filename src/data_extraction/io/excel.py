from pathlib import Path
import re

import pandas as pd


def export_excel_sheets_to_csv(
    excel_path: str | Path,
    output_dir: str | Path = "data/csv",
    *,
    verbose: bool = True,
) -> list[Path]:
    """Export each sheet of an Excel file to a separate CSV file."""
    excel_path = Path(excel_path)
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    xls = pd.ExcelFile(excel_path)
    csv_paths: list[Path] = []

    for sheet_name in xls.sheet_names:
        safe_name = re.sub(r"[<>:\"/\\|?*\x00-\x1F]+", "_", sheet_name).strip() or "sheet"
        csv_path = output_dir / f"{safe_name}.csv"

        df = pd.read_excel(xls, sheet_name=sheet_name)
        df.to_csv(csv_path, index=False)
        csv_paths.append(csv_path)

        if verbose:
            print(f"Saved: {csv_path}")

    if verbose:
        print(f"Done. Exported {len(csv_paths)} sheet(s) to {output_dir.resolve()}")

    return csv_paths

