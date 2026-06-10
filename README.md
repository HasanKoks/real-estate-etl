# Real Estate Market and Pricing ETL Pipeline

An end to end Python ETL pipeline that integrates 8 relational data
sources used in real estate market and pricing analysis. The
pipeline cleans and joins listings, transactions, agents, regions,
property attributes, market indices, mortgage rates, and a
calendar dimension into a single analytical fact table, then
produces a monthly market and pricing summary ready for Power BI.

Built to mirror the kind of pipeline I worked on at REMAX Luna,
where market and pricing data lived in separate sources and needed
to be reconciled before any reporting or pricing decision could be
made.

## Problem
Real estate teams typically work with data scattered across many
operational systems: a listings system, a closed deal record, an
agent CRM, regional reference data, mortgage rates, and external
market indices. Pulling these together by hand each month is slow
and breaks easily. This pipeline automates the full flow from raw
files to a clean, query ready table and a monthly summary CSV.

## Pipeline overview

Extract reads 8 raw CSV sources from data/raw: listings,
transactions, agents, regions, property attributes, market index,
mortgage rates, and a calendar dimension.

Transform cleans the data, handles missing values, parses dates,
joins all 8 sources into a single property_fact table, and
calculates derived fields including price per square meter, days
on market, and an asking versus closing price gap.

Load writes the fact table into a local SQLite database, ready
for SQL queries or BI tools.

Report runs a SQL query that produces a monthly market and
pricing summary by region and property type, saved as a CSV in
data/processed.

## What the pipeline produces
A property_fact table with one row per closed transaction,
enriched with agent, region, property attribute, market index,
and mortgage context, plus a monthly_market_summary.csv ready to
drop into Power BI.

## Tools
Python, Pandas, SQLAlchemy, SQLite, pytest

## How to run

```
git clone https://github.com/HasanKoks/real-estate-etl
cd real-estate-etl
pip install -r requirements.txt
python src/generate_data.py
python src/run_pipeline.py
```

After running, the SQLite database appears at
data/processed/real_estate.db and the monthly summary at
data/processed/monthly_market_summary.csv.

## Project structure

```
real-estate-etl/
  src/
    extract.py        reads the 8 raw CSVs
    transform.py      cleaning, joining, feature creation
    load.py           writes to SQLite, runs the summary query
    run_pipeline.py   orchestrates extract, transform, load
    generate_data.py  builds synthetic sample data
  sql/
    monthly_market_summary.sql
  data/
    raw/              the 8 input CSVs
    processed/        the SQLite db and summary csv
  notebooks/
    exploration.ipynb optional ad hoc analysis
  tests/
    test_transform.py
  requirements.txt
```

## Notes on the data
The CSVs in data/raw are synthetic, generated to mimic the shape
and scale of real estate data I worked with at REMAX Luna. No real
listing or client information is used.
