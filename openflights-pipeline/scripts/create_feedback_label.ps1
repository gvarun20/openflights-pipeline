# One-time: create the "feedback" label for dashboard visitor comments.
# Requires GitHub CLI: https://cli.github.com
#
#   gh auth login
#   .\scripts\create_feedback_label.ps1

$ErrorActionPreference = "Stop"
gh label create feedback `
  --repo gvarun20/openflights-pipeline `
  --description "Visitor feedback from the live dashboard" `
  --color 3b82f6 `
  --force
Write-Host "Done. Label 'feedback' is ready."
