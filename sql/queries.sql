-- 1. CTE: top 10 busiest airports by total routes (as source OR destination)
WITH airport_traffic AS (
    SELECT src_airport_id AS airport_id, COUNT(*) AS outbound FROM fact_routes GROUP BY 1
    UNION ALL
    SELECT dst_airport_id, COUNT(*) AS inbound FROM fact_routes GROUP BY 1
)
SELECT a.name, a.country, SUM(t.outbound) AS total_routes
FROM airport_traffic t
JOIN dim_airport a ON a.airport_id = t.airport_id
GROUP BY a.name, a.country
ORDER BY total_routes DESC
LIMIT 10;

-- 2. Window function: rank airlines by route count within each country
SELECT
    al.country,
    al.name AS airline,
    COUNT(r.route_id) AS routes,
    RANK() OVER (PARTITION BY al.country ORDER BY COUNT(r.route_id) DESC) AS country_rank
FROM fact_routes r
JOIN dim_airline al ON al.airline_id = r.airline_id
GROUP BY al.country, al.name
ORDER BY al.country, country_rank;

-- 3. Window function: running total of routes added per airline
SELECT
    al.name,
    r.loaded_at::DATE AS load_date,
    COUNT(*) AS daily_routes,
    SUM(COUNT(*)) OVER (PARTITION BY al.airline_id ORDER BY r.loaded_at::DATE) AS cumulative_routes
FROM fact_routes r
JOIN dim_airline al ON al.airline_id = r.airline_id
GROUP BY al.name, al.airline_id, load_date
ORDER BY al.name, load_date;

-- 4. Self-join: find routes that exist in BOTH directions (A→B and B→A)
SELECT
    a1.iata_code AS origin,
    a2.iata_code AS destination
FROM fact_routes r1
JOIN fact_routes r2
    ON r1.src_airport_id = r2.dst_airport_id
    AND r1.dst_airport_id = r2.src_airport_id
JOIN dim_airport a1 ON a1.airport_id = r1.src_airport_id
JOIN dim_airport a2 ON a2.airport_id = r1.dst_airport_id
WHERE r1.src_airport_id < r1.dst_airport_id;  -- avoid duplicates

-- 5. CTE + window: find airports with NO outbound routes (data quality check)
WITH all_src AS (
    SELECT DISTINCT src_airport_id FROM fact_routes
)
SELECT a.airport_id, a.name, a.country
FROM dim_airport a
LEFT JOIN all_src s ON s.src_airport_id = a.airport_id
WHERE s.src_airport_id IS NULL;

-- 6. Execution plan analysis — run EXPLAIN ANALYZE on this and document findings
EXPLAIN ANALYZE
SELECT al.country, COUNT(DISTINCT r.dst_airport_id) AS unique_destinations
FROM fact_routes r
JOIN dim_airline al ON al.airline_id = r.airline_id
GROUP BY al.country
ORDER BY unique_destinations DESC;