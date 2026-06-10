-- Monthly market and pricing summary by region and property type.
-- Feeds the Power BI market dashboard.

SELECT
    year_month,
    region_name,
    property_type,
    COUNT(*)                              AS transactions,
    ROUND(AVG(closing_price), 0)          AS avg_closing_price,
    ROUND(AVG(price_per_m2), 0)           AS avg_price_per_m2,
    ROUND(AVG(days_on_market), 1)         AS avg_days_on_market,
    ROUND(AVG(price_gap_pct), 2)          AS avg_price_gap_pct,
    ROUND(AVG(market_index), 2)           AS market_index,
    ROUND(AVG(mortgage_rate), 2)          AS mortgage_rate
FROM property_fact
GROUP BY year_month, region_name, property_type
ORDER BY year_month, region_name, property_type;
