# Open Flights Data Pipeline

## Project Overview
A data warehouse for Open Flights data with a star schema design.

## Schema Design

### Star Schema Architecture
The design uses a star schema with:
- **Fact table**: `fact_routes` (routes, airlines, equipment)
- **Dimensions**: airports, airlines, equipment, date

### Key Design Decisions

#### 1. Star vs Snowflake
**Decision**: Star schema (no further normalization)
**Why**: Query simplicity. Airports don't normalize further (country is rare to aggregate separately). Storage cost is negligible.

#### 2. Two FKs to dim_airport (Role-Playing Dimension)
**Decision**: `src_airport_id` and `dst_airport_id` both reference `dim_airport`
**Why**: A route has an origin and destination — both are airports. Rather than duplicate the table, we use role-playing: same dimension, two roles.

#### 3. SCD Type 2 on dim_airline
**Decision**: Columns `valid_from`, `valid_to`, `is_current`
**Why**: Airlines merge, rename, go bankrupt. We preserve history. Queries filter `WHERE is_current = TRUE` for current state.

#### 4. dim_date as a Separate Table
**Decision**: Include date dimension even though routes don't have timestamps yet
**Why**: Future-proofs the schema. When flight schedules are added, date fields are ready. Enables day-of-week, season, holiday analytics.

#### 5. Indexes on Foreign Keys Only
**Decision**: `idx_fact_src`, `idx_fact_dst`, `idx_fact_airl` on fact table FKs
**Why**: JOINs use these columns. We didn't index every column (premature optimization).

## SQL Queries

See `sql/queries.sql` for:
- Top 10 busiest airports (CTEs)
- Airlines ranked by country (window functions)
- Running totals (OVER clauses)
- Bidirectional routes (self-joins)
- Data quality checks (missing sources)
- EXPLAIN ANALYZE results

## Next Steps (Phase 2)
Python ETL pipeline to load raw .dat files into these tables.