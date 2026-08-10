"""Copy demo_data.json to docs/ with pipeline_status (no DB required)."""

import json
import sys
from datetime import date, datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DEMO = ROOT / "dashboard" / "demo_data.json"
DOCS = ROOT.parent / "docs"


CHECKS_FILE = ROOT / "quality" / "checks.yml"


def count_soda_checks() -> int:
    return sum(
        1 for line in CHECKS_FILE.read_text(encoding="utf-8").splitlines() if line.startswith("  - ")
    )


def main() -> int:
    if not DEMO.exists():
        print(f"Missing {DEMO}", file=sys.stderr)
        return 1

    data = json.loads(DEMO.read_text(encoding="utf-8"))
    today = date.today().isoformat()
    status = {
        "last_export_utc": datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC"),
        "generated_at": today,
        "quality_passed": True,
        "routes_loaded": data["kpis"]["routes"],
        "soda_checks": count_soda_checks(),
        "status": "healthy",
    }
    data["generated_at"] = today
    data["pipeline_status"] = status

    json_text = json.dumps(data, indent=2)
    DOCS.mkdir(exist_ok=True)
    (DOCS / "data.json").write_text(json_text + "\n", encoding="utf-8")
    (DOCS / "data.js").write_text(
        "window.DASHBOARD_DATA = " + json.dumps(data) + ";\n",
        encoding="utf-8",
    )
    (DOCS / "status.json").write_text(json.dumps(status, indent=2) + "\n", encoding="utf-8")
    print(f"Synced {DOCS / 'data.json'}")
    print(f"Synced {DOCS / 'status.json'}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
