# OpenFlights pipeline — common commands (Git Bash / WSL / macOS / Linux)
.PHONY: etl test quality dashboard pipeline help

help:
	@echo "OpenFlights pipeline commands:"
	@echo "  make etl        - Run ETL + data quality checks"
	@echo "  make test       - Run all tests (unit + integration; needs loaded DB for integration)"
	@echo "  make test-unit  - Run unit tests only"
	@echo "  make quality    - Run Soda data quality checks"
	@echo "  make dashboard  - Export dashboard JSON from PostgreSQL"
	@echo "  make pipeline   - ETL + quality + dashboard export"

etl:
	python -m etl.run_etl --init --validate

quality:
	python -m quality.run_checks -v

dashboard:
	python dashboard/export_snapshot.py

test-unit:
	python -m pytest tests/ -v -m "not integration"

test:
	python -m pytest tests/ -v

pipeline: etl dashboard
	@echo "Pipeline complete."
