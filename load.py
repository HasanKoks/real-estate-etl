"""
Load step. Writes the property fact table into a local SQLite
database and runs the monthly market summary query against it,
saving the result as a CSV.
"""
from pathlib import Path
import pandas as pd
from sqlalchemy import create_engine, text

PROCESSED = Path(__file__).resolve().parents[1] / "data" / "processed"
SQL_DIR = Path(__file__).resolve().parents[1] / "sql"
DB_PATH = PROCESSED / "real_estate.db"


def load_to_sqlite(property_fact: pd.DataFrame) -> None:
    PROCESSED.mkdir(parents=True, exist_ok=True)
    engine = create_engine(f"sqlite:///{DB_PATH}")
    property_fact.to_sql("property_fact", engine,
                         if_exists="replace", index=False)


def export_monthly_market_summary() -> pd.DataFrame:
    engine = create_engine(f"sqlite:///{DB_PATH}")
    query = (SQL_DIR / "monthly_market_summary.sql").read_text()
    with engine.connect() as conn:
        summary = pd.read_sql(text(query), conn)
    summary.to_csv(PROCESSED / "monthly_market_summary.csv", index=False)
    return summary
