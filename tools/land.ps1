#requires -Version 5
# land.ps1 - land a thin bundle onto the canonical repo from the Owner's machine.
# Tier 2 of docs/LANDING-PROTOCOL.md. Claude runs this through the desktop local shell;
# credentials stay in the Owner's Git Credential Manager and never enter the sandbox.
# Fast-forward only, everywhere. Never force-pushes, never rebases.
[CmdletBinding()]
param(
  [Parameter(Mandatory = $true)][string]$Bundle,
  [string]$Repo   = "C:\Users\chris\autonomy-system-live",
  [string]$Branch = "main",
  [string]$Remote = "origin"
)
# MUST stay 'Continue'. git writes progress to stderr on SUCCESS (fetch, checkout, push);
# under 'Stop' PowerShell 5 wraps that as a terminating NativeCommandError and kills a
# healthy run. Success is decided by $LASTEXITCODE alone, never by stderr being non-empty.
$ErrorActionPreference = "Continue"

function Invoke-Git {                     # a REAL step: non-zero exit is fatal
  param([string[]]$GitArgs, [string]$Fail)
  $out = & git @GitArgs 2>&1
  foreach ($line in $out) { Write-Host "  $line" }
  if ($LASTEXITCODE -ne 0) { Write-Host "LAND FAILED: $Fail" -ForegroundColor Red; exit 1 }
}
function Remove-LandBranch {              # never call branch -D on a branch that is absent
  & git show-ref --verify --quiet refs/heads/land-incoming 2>&1 | Out-Null
  if ($LASTEXITCODE -eq 0) { & git branch -D land-incoming 2>&1 | Out-Null }
}

if (-not (Test-Path -LiteralPath $Repo)) {
  Write-Host "LAND FAILED: standing clone not found at $Repo" -ForegroundColor Red
  Write-Host "Recreate it: git clone https://github.com/chrispcariello/autonomy-system.git $Repo"
  exit 1
}
if (-not (Test-Path -LiteralPath $Bundle)) {
  Write-Host "LAND FAILED: bundle not found at $Bundle" -ForegroundColor Red; exit 1
}
Set-Location -LiteralPath $Repo

Invoke-Git @("fetch", $Remote) "cannot reach $Remote - check network and Git Credential Manager"
Invoke-Git @("checkout", $Branch) "cannot check out $Branch - commit or stash local changes first"
Invoke-Git @("merge", "--ff-only", "$Remote/$Branch") "local $Branch has diverged from $Remote/$Branch - resolve by hand, do not force"

Remove-LandBranch                          # drop any leftover from a failed run
Invoke-Git @("fetch", $Bundle, "${Branch}:land-incoming") "bundle unreadable or has no '$Branch' ref - rebuild it"
Invoke-Git @("merge", "--ff-only", "land-incoming") "bundle base is stale; rebuild bundle on current tip"
Invoke-Git @("push", $Remote, $Branch) "push rejected - re-run this script to re-sync, never force"

Remove-LandBranch                          # housekeeping only - the landing already succeeded
& git show-ref --verify --quiet refs/heads/land-incoming 2>&1 | Out-Null
if ($LASTEXITCODE -eq 0) { Write-Host "WARNING: landed and pushed, but land-incoming still exists" -ForegroundColor Yellow }

$sha = "$(& git rev-parse --short HEAD)".Trim()
Write-Host "LANDED $sha on $Branch" -ForegroundColor Green
exit 0
