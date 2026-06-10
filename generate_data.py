"""
Generates 8 synthetic CSV sources mimicking real estate data
across listings, transactions, agents, regions, property
attributes, market index, mortgage rates, and a calendar.

Run once to populate data/raw.
"""
import numpy as np
import pandas as pd
from pathlib import Path

RAW = Path(__file__).resolve().parents[1] / "data" / "raw"
RAW.mkdir(parents=True, exist_ok=True)

rng = np.random.default_rng(42)

N_REGIONS = 6
N_AGENTS = 40
N_PROPERTIES = 5000
N_TRANSACTIONS = 3500

region_names = ["Kadikoy", "Besiktas", "Sisli", "Uskudar", "Bakirkoy", "Maltepe"]
property_types = ["Apartment", "Detached House", "Penthouse", "Studio", "Duplex"]

# 1, regions
regions = pd.DataFrame({
    "region_id": [f"R{i+1:02d}" for i in range(N_REGIONS)],
    "region_name": region_names,
    "city": "Istanbul",
    "avg_income_index": np.round(rng.uniform(80, 140, N_REGIONS), 1),
})
regions.to_csv(RAW / "regions.csv", index=False)

# 2, agents
agents = pd.DataFrame({
    "agent_id": [f"A{i+1:03d}" for i in range(N_AGENTS)],
    "agent_name": [f"Agent {i+1}" for i in range(N_AGENTS)],
    "region_id": rng.choice(regions["region_id"], N_AGENTS),
    "years_experience": rng.integers(1, 20, N_AGENTS),
})
agents.to_csv(RAW / "agents.csv", index=False)

# 3, property attributes, one row per property
property_attrs = pd.DataFrame({
    "property_id": [f"P{i+1:05d}" for i in range(N_PROPERTIES)],
    "region_id": rng.choice(regions["region_id"], N_PROPERTIES),
    "property_type": rng.choice(property_types, N_PROPERTIES),
    "size_m2": rng.integers(40, 280, N_PROPERTIES),
    "rooms": rng.integers(1, 6, N_PROPERTIES),
    "year_built": rng.integers(1970, 2024, N_PROPERTIES),
    "has_parking": rng.choice([0, 1], N_PROPERTIES, p=[0.4, 0.6]),
})
property_attrs.to_csv(RAW / "property_attributes.csv", index=False)

# 4, listings, asking price when first listed
listings = property_attrs[["property_id", "size_m2"]].copy()
base_price = listings["size_m2"] * rng.uniform(18000, 42000, N_PROPERTIES)
listings["asking_price"] = np.round(base_price * rng.uniform(0.85, 1.25, N_PROPERTIES), 0)
listings["listed_date"] = pd.to_datetime(
    rng.integers(
        pd.Timestamp("2023-01-01").value // 10**9,
        pd.Timestamp("2024-10-01").value // 10**9,
        N_PROPERTIES,
    ),
    unit="s",
).strftime("%Y-%m-%d")
listings = listings[["property_id", "listed_date", "asking_price"]]
listings.to_csv(RAW / "listings.csv", index=False)

# 5, transactions, closed deals, subset of properties
tx_props = rng.choice(property_attrs["property_id"], N_TRANSACTIONS, replace=False)
tx_listed = listings.set_index("property_id").loc[tx_props].reset_index()
close_offsets = rng.integers(10, 240, N_TRANSACTIONS)
close_dates = pd.to_datetime(tx_listed["listed_date"]) + pd.to_timedelta(close_offsets, unit="D")
closing_price = np.round(tx_listed["asking_price"] * rng.uniform(0.85, 1.05, N_TRANSACTIONS), 0)

transactions = pd.DataFrame({
    "transaction_id": [f"T{i+1:05d}" for i in range(N_TRANSACTIONS)],
    "property_id": tx_props,
    "agent_id": rng.choice(agents["agent_id"], N_TRANSACTIONS),
    "closing_date": close_dates.dt.strftime("%Y-%m-%d"),
    "closing_price": closing_price,
})
# inject realistic messiness
transactions.loc[rng.choice(N_TRANSACTIONS, 40, replace=False), "closing_price"] = np.nan
transactions.loc[rng.choice(N_TRANSACTIONS, 15, replace=False), "closing_date"] = ""
transactions.to_csv(RAW / "transactions.csv", index=False)

# 6, market index, monthly
months = pd.date_range("2023-01-01", "2024-12-01", freq="MS")
market_index = pd.DataFrame({
    "year_month": months.strftime("%Y-%m"),
    "market_index": np.round(100 + np.cumsum(rng.normal(0.4, 0.8, len(months))), 2),
})
market_index.to_csv(RAW / "market_index.csv", index=False)

# 7, mortgage rates, monthly
mortgage_rates = pd.DataFrame({
    "year_month": months.strftime("%Y-%m"),
    "mortgage_rate": np.round(rng.uniform(1.5, 4.5, len(months)), 2),
})
mortgage_rates.to_csv(RAW / "mortgage_rates.csv", index=False)

# 8, calendar dimension
calendar = pd.DataFrame({
    "date": pd.date_range("2023-01-01", "2024-12-31", freq="D").strftime("%Y-%m-%d"),
})
calendar["year"] = pd.to_datetime(calendar["date"]).dt.year
calendar["month"] = pd.to_datetime(calendar["date"]).dt.month
calendar["quarter"] = pd.to_datetime(calendar["date"]).dt.quarter
calendar["year_month"] = pd.to_datetime(calendar["date"]).dt.strftime("%Y-%m")
calendar.to_csv(RAW / "calendar.csv", index=False)

print("Generated 8 raw sources in", RAW)
for f in sorted(RAW.glob("*.csv")):
    print(f"  {f.name:30s} {sum(1 for _ in open(f))-1:>6d} rows")
