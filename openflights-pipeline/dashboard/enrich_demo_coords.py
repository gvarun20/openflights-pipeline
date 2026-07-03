"""One-off helper: add lat/lon to demo_data.json from airports.dat (no DB needed)."""

import json
from pathlib import Path

DASHBOARD = Path(__file__).resolve().parent
DATA = DASHBOARD / "demo_data.json"
AIRPORTS = DASHBOARD.parent / "data" / "airports.dat"

IATA_COORDS: dict[str, tuple[float, float]] = {}


def load_coords() -> None:
    for line in AIRPORTS.read_text(encoding="utf-8").splitlines():
        parts = line.split(",")
        if len(parts) < 8:
            continue
        iata = parts[4].strip().strip('"')
        if iata in ("", "\\N"):
            continue
        try:
            lat = float(parts[6])
            lon = float(parts[7])
        except ValueError:
            continue
        IATA_COORDS[iata] = (lat, lon)


def main() -> None:
    load_coords()
    data = json.loads(DATA.read_text(encoding="utf-8"))

    for apt in data.get("top_airports", []):
        coords = IATA_COORDS.get(apt["iata"])
        if coords:
            apt["latitude"], apt["longitude"] = coords

    for pair in data.get("top_route_pairs", []):
        src = IATA_COORDS.get(pair["from_iata"])
        dst = IATA_COORDS.get(pair["to_iata"])
        if src:
            pair["from_lat"], pair["from_lon"] = src
        if dst:
            pair["to_lat"], pair["to_lon"] = dst

    DATA.write_text(json.dumps(data, indent=2), encoding="utf-8")
    print(f"Updated {DATA}")


if __name__ == "__main__":
    main()
