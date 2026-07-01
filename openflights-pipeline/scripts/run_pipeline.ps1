# Run the full OpenFlights pipeline locally (ETL + quality + dashboard export).
# Requires PostgreSQL running and .env configured — see DOCUMENTATION.md.

$ErrorActionPreference = "Stop"
Set-Location (Join-Path $PSScriptRoot "..")

Write-Host "==> Running ETL with data quality checks..." -ForegroundColor Cyan
py -m etl.run_etl --init --validate
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

Write-Host "==> Exporting dashboard snapshot..." -ForegroundColor Cyan
py dashboard/export_snapshot.py
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

Write-Host "==> Pipeline complete." -ForegroundColor Green
