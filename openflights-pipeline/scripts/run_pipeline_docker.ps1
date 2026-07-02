# Run the full pipeline inside Docker (Option 2 stack).
# See DOCKER.md for the learning path.

$ErrorActionPreference = "Stop"
Set-Location (Join-Path $PSScriptRoot "..")

Write-Host "==> Starting Postgres..." -ForegroundColor Cyan
docker compose --profile pipeline up -d postgres
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

Write-Host "==> Running ETL + quality checks..." -ForegroundColor Cyan
docker compose --profile pipeline run --rm etl
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

Write-Host "==> Exporting dashboard snapshot..." -ForegroundColor Cyan
docker compose --profile pipeline run --rm export
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

Write-Host "==> Docker pipeline complete." -ForegroundColor Green
Write-Host "    pgAdmin:    http://localhost:5050  (docker compose --profile dev up -d)" -ForegroundColor DarkGray
Write-Host "    Dashboard:  http://localhost:8080" -ForegroundColor DarkGray
