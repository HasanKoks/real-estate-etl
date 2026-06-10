"""
Extract step. Reads all 8 raw CSV sources into pandas DataFrames.
"""
from pathlib import Path
import pandas as pd

RAW = Path(__file__).resolve().parents[1] / "data" / "raw"


def extract_all() -> dict:
    return {
        "listings": pd.read_csv(RAW / "listings.csv",
                                parse_dates=["listed_date"]),
        "transactions": pd.read_csv(RAW / "transactions.csv"),
        "agents": pd.read_csv(RAW / "agents.csv"),
        "regions": pd.read_csv(RAW / "regions.csv"),
        "property_attrs": pd.read_csv(RAW / "property_attributes.csv"),
        "market_index": pd.read_csv(RAW / "market_index.csv"),
        "mortgage_rates": pd.read_csv(RAW / "mortgage_rates.csv"),
        "calendar": pd.read_csv(RAW / "calendar.csv",
                                parse_dates=["date"]),
    }
