-- dim_airport
CREATE TABLE dim_airport (
    airport_id    SERIAL PRIMARY KEY,
    name          TEXT NOT NULL,
    city          TEXT,
    country       TEXT,
    iata_code     CHAR(3),
    icao_code     CHAR(4),
    latitude      NUMERIC(9,6),
    longitude     NUMERIC(9,6),
    altitude_ft   INT,
    timezone_utc  NUMERIC(4,1)
);

-- dim_airline (with SCD type 2 columns)
CREATE TABLE dim_airline (
    airline_id      SERIAL PRIMARY KEY,
    name            TEXT NOT NULL,
    iata_code       CHAR(2),
    icao_code       CHAR(3),
    country         TEXT,
    active          BOOLEAN,
    valid_from      DATE NOT NULL DEFAULT CURRENT_DATE,
    valid_to        DATE,
    is_current      BOOLEAN DEFAULT TRUE
);

-- dim_equipment
CREATE TABLE dim_equipment (
    equipment_id   SERIAL PRIMARY KEY,
    iata_code      CHAR(3) UNIQUE,
    aircraft_name  TEXT,
    category       TEXT  -- 'narrowbody','widebody','regional','turboprop'
);

-- dim_date
CREATE TABLE dim_date (
    date_id    INT PRIMARY KEY,  -- YYYYMMDD format
    full_date  DATE NOT NULL,
    year       INT,
    quarter    INT,
    month      INT,
    month_name TEXT,
    day        INT,
    weekday    TEXT,
    is_weekend BOOLEAN,
    season     TEXT
);

-- fact_routes (the centre of the star)
CREATE TABLE fact_routes (
    route_id        SERIAL PRIMARY KEY,
    airline_id      INT REFERENCES dim_airline(airline_id),
    src_airport_id  INT REFERENCES dim_airport(airport_id),
    dst_airport_id  INT REFERENCES dim_airport(airport_id),
    equipment_id    INT REFERENCES dim_equipment(equipment_id),
    codeshare       BOOLEAN DEFAULT FALSE,
    stops           INT DEFAULT 0,
    loaded_at       TIMESTAMP DEFAULT NOW()
);

-- indexes for query performance
CREATE INDEX idx_fact_src  ON fact_routes(src_airport_id);
CREATE INDEX idx_fact_dst  ON fact_routes(dst_airport_id);
CREATE INDEX idx_fact_airl ON fact_routes(airline_id);