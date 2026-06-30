import csv
from pathlib import Path
from typing import Iterator, Optional


def parse_null(value: str) -> Optional[str]:
    if value in ("", "\\N", "-"):
        return None
    return value


def parse_fixed_code(value: str, length: int) -> Optional[str]:
    cleaned = parse_null(value)
    if cleaned is None or len(cleaned) != length:
        return None
    return cleaned


def parse_bool_yn(value: str) -> Optional[bool]:
    if value in ("", "\\N"):
        return None
    return value.upper() == "Y"


def parse_int(value: str) -> Optional[int]:
    cleaned = parse_null(value)
    if cleaned is None:
        return None
    return int(cleaned)


def parse_float(value: str) -> Optional[float]:
    cleaned = parse_null(value)
    if cleaned is None:
        return None
    return float(cleaned)


def read_csv_rows(path: Path) -> Iterator[list[str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        reader = csv.reader(handle)
        for row in reader:
            yield row


def parse_airports(path: Path) -> Iterator[dict]:
    for row in read_csv_rows(path):
        yield {
            "airport_id": int(row[0]),
            "name": row[1],
            "city": parse_null(row[2]),
            "country": parse_null(row[3]),
            "iata_code": parse_fixed_code(row[4], 3),
            "icao_code": parse_fixed_code(row[5], 4),
            "latitude": parse_float(row[6]),
            "longitude": parse_float(row[7]),
            "altitude_ft": parse_int(row[8]),
            "timezone_utc": parse_float(row[9]),
        }


def parse_airlines(path: Path) -> Iterator[dict]:
    for row in read_csv_rows(path):
        yield {
            "airline_id": int(row[0]),
            "name": row[1],
            "iata_code": parse_fixed_code(row[3], 2),
            "icao_code": parse_fixed_code(row[4], 3),
            "country": parse_null(row[6]),
            "active": parse_bool_yn(row[7]),
        }


def parse_equipment(path: Path) -> Iterator[dict]:
    for row in read_csv_rows(path):
        iata_code = parse_fixed_code(row[1], 3)
        if iata_code is None:
            continue
        yield {
            "iata_code": iata_code,
            "aircraft_name": row[0],
            "category": None,
        }


def parse_routes(path: Path) -> Iterator[dict]:
    for row in read_csv_rows(path):
        yield {
            "airline_id": parse_int(row[1]),
            "src_airport_id": parse_int(row[3]),
            "dst_airport_id": parse_int(row[5]),
            "codeshare": row[6].upper() == "Y" if row[6] else False,
            "stops": parse_int(row[7]) or 0,
            "equipment_iata": parse_null(row[8]),
        }
