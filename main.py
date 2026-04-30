from pathlib import Path
import sys


sys.path.insert(0, str(Path(__file__).resolve().parent / "src"))

from data_extraction.io.excel import export_excel_sheets_to_csv


def main():
    """Export the default WAFCT workbook to CSV files."""
    export_excel_sheets_to_csv("data/xlsx/WAFCT_2019.xlsx", "data/csv")


if __name__ == "__main__":
    main()
