"""
Transform step. Cleans transactions, joins all 8 sources into a
single property_fact table, and computes derived fields used in
pricing and market analysis.
"""
import pandas as pd


def clean_transactions(transactions: pd.DataFrame) -> pd.DataFrame:
    """Drop rows with no closing date or price, parse the date."""
    df = transactions.copy()
    df["closing_date"] = pd.to_datetime(df["closing_date"], errors="coerce")
    df = df.dropna(subset=["closing_date", "closing_price"])
    df["closing_price"] = df["closing_price"].astype(float)
    return df


def build_property_fact(sources: dict) -> pd.DataFrame:
    """Join the 8 sources into a single analytical fact table."""
    tx = clean_transactions(sources["transactions"])

    df = (
        tx
        .merge(sources["listings"], on="property_id", how="left")
        .merge(sources["property_attrs"], on="property_id", how="left")
        .merge(sources["agents"][["agent_id", "agent_name", "years_experience"]],
               on="agent_id", how="left")
        .merge(sources["regions"], on="region_id", how="left")
    )

    df["year_month"] = df["closing_date"].dt.to_period("M").astype(str)

    df = df.merge(sources["market_index"], on="year_month", how="left")
    df = df.merge(sources["mortgage_rates"], on="year_month", how="left")

    # derived fields used for pricing decisions
    df["price_per_m2"] = (df["closing_price"] / df["size_m2"]).round(2)
    df["days_on_market"] = (df["closing_date"] - df["listed_date"]).dt.days
    df["price_gap_pct"] = (
        (df["closing_price"] - df["asking_price"]) / df["asking_price"] * 100
    ).round(2)

    cols = [
        "transaction_id", "property_id", "closing_date", "year_month",
        "region_id", "region_name", "city", "avg_income_index",
        "property_type", "size_m2", "rooms", "year_built", "has_parking",
        "agent_id", "agent_name", "years_experience",
        "listed_date", "asking_price", "closing_price",
        "price_per_m2", "days_on_market", "price_gap_pct",
        "market_index", "mortgage_rate",
    ]
    return df[cols]


def transform(sources: dict) -> pd.DataFrame:
    return build_property_fact(sources)
