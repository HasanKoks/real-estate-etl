"""
Tests for the transform step. Run from the project root: pytest
"""
import sys
from pathlib import Path
import pandas as pd
import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from transform import clean_transactions, build_property_fact


def test_clean_transactions_drops_missing():
    df = pd.DataFrame({
        "transaction_id": ["T1", "T2", "T3", "T4"],
        "property_id": ["P1", "P2", "P3", "P4"],
        "agent_id": ["A1", "A1", "A2", "A2"],
        "closing_date": ["2024-01-01", "", "2024-02-01", "2024-03-01"],
        "closing_price": [100000.0, 120000.0, np.nan, 150000.0],
    })
    cleaned = clean_transactions(df)
    assert len(cleaned) == 2
    assert cleaned["closing_price"].isna().sum() == 0


def test_build_property_fact_derived_fields():
    sources = {
        "transactions": pd.DataFrame({
            "transaction_id": ["T1"],
            "property_id": ["P1"],
            "agent_id": ["A1"],
            "closing_date": ["2024-05-10"],
            "closing_price": [200000.0],
        }),
        "listings": pd.DataFrame({
            "property_id": ["P1"],
            "listed_date": pd.to_datetime(["2024-04-10"]),
            "asking_price": [180000.0],
        }),
        "property_attrs": pd.DataFrame({
            "property_id": ["P1"], "region_id": ["R01"],
            "property_type": ["Apartment"], "size_m2": [100],
            "rooms": [3], "year_built": [2010], "has_parking": [1],
        }),
        "agents": pd.DataFrame({
            "agent_id": ["A1"], "agent_name": ["X"],
            "region_id": ["R01"], "years_experience": [5],
        }),
        "regions": pd.DataFrame({
            "region_id": ["R01"], "region_name": ["Kadikoy"],
            "city": ["Istanbul"], "avg_income_index": [110.0],
        }),
        "market_index": pd.DataFrame({
            "year_month": ["2024-05"], "market_index": [105.0],
        }),
        "mortgage_rates": pd.DataFrame({
            "year_month": ["2024-05"], "mortgage_rate": [2.5],
        }),
        "calendar": pd.DataFrame(),
    }
    fact = build_property_fact(sources)
    row = fact.iloc[0]
    assert row["price_per_m2"] == 2000.0
    assert row["days_on_market"] == 30
    assert round(row["price_gap_pct"], 2) == 11.11
    assert row["year_month"] == "2024-05"
