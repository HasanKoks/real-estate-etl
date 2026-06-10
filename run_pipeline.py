"""
Orchestrates the full pipeline: extract, transform, load,
then export the monthly market and pricing summary.

Run from the project root:
    python src/run_pipeline.py
"""
from extract import extract_all
from transform import transform
from load import load_to_sqlite, export_monthly_market_summary


def main() -> None:
    print("[1/4] Extracting 8 raw sources...")
    sources = extract_all()
    for name, df in sources.items():
        print(f"      {name:18s} {len(df):>6d} rows")

    print("[2/4] Transforming and joining...")
    property_fact = transform(sources)
    print(f"      property_fact rows: {len(property_fact)}")
    print(f"      avg price per m2:   {property_fact['price_per_m2'].mean():,.0f}")
    print(f"      median days on mkt: {property_fact['days_on_market'].median():.0f}")

    print("[3/4] Loading into SQLite...")
    load_to_sqlite(property_fact)

    print("[4/4] Exporting monthly market summary...")
    summary = export_monthly_market_summary()
    print(f"      summary rows: {len(summary)}")
    print("\nDone. Outputs:")
    print("  data/processed/real_estate.db")
    print("  data/processed/monthly_market_summary.csv")


if __name__ == "__main__":
    main()
