from dotenv import load_dotenv


DEFAULT_CSV_PATH = "data/csv/04 NV_stat_39 (per 100g EP).csv"
DEFAULT_OUTPUT_PATH = "data/json/04_NV_stat_39_structured.json"
DEFAULT_MODEL = "gpt-5-mini"
DEFAULT_GEOGRAPHICAL_AREA = "West Africa"


def load_env(path: str = ".env") -> None:
    load_dotenv(dotenv_path=path, override=False)
