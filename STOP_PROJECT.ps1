# ==============================================================================
# STOP_PROJECT.ps1 — Graceful Teardown Script for KubeCostFinOps
# KubeCostFinOps: Kubernetes Cost Optimization Framework (BCSE355L)
# Institution: VIT Vellore • Team Lead: K. Darshan
# Operating System: Windows 11 PowerShell
# ==============================================================================

[CmdletBinding()]
param(
    [int]$Port = 8000
)

$ErrorActionPreference = "SilentlyContinue"

Write-Host ""
Write-Host "===========================================================================" -ForegroundColor Cyan
Write-Host "  STOPPING KUBECOST FINOPS BACKEND SERVICES" -ForegroundColor Cyan
Write-Host "===========================================================================" -ForegroundColor Cyan
Write-Host ""

$pidFile = ".backend.pid"
$stopped = $false

# 1. Stop by recorded PID file
if (Test-Path $pidFile) {
    try {
        $savedPid = Get-Content $pidFile | ForEach-Object { [int]$_ }
        if ($savedPid -gt 0) {
            $p = Get-Process -Id $savedPid -ErrorAction SilentlyContinue
            if ($p) {
                Write-Host "[INFO] Stopping backend process (PID: $savedPid)..." -ForegroundColor Cyan
                Stop-Process -Id $savedPid -Force -ErrorAction SilentlyContinue
                $stopped = $true
            }
        }
    } catch {
        # Continue
    }
    Remove-Item -Path $pidFile -Force -ErrorAction SilentlyContinue
}

# 2. Check for any remaining listener on port 8000
$conns = Get-NetTCPConnection -LocalPort $Port -ErrorAction SilentlyContinue | Where-Object { $_.State -eq "Listen" }
if ($conns) {
    foreach ($conn in $conns) {
        $owningPid = $conn.OwningProcess
        if ($owningPid -gt 0) {
            $p = Get-Process -Id $owningPid -ErrorAction SilentlyContinue
            if ($p -and $p.ProcessName -match "python") {
                Write-Host "[INFO] Releasing port $Port held by process PID $owningPid ($($p.ProcessName))..." -ForegroundColor Cyan
                Stop-Process -Id $owningPid -Force -ErrorAction SilentlyContinue
                $stopped = $true
            }
        }
    }
}

Start-Sleep -Milliseconds 800

# 3. Verify port is completely free
$verify = Get-NetTCPConnection -LocalPort $Port -State Listen -ErrorAction SilentlyContinue
if ($verify -and $verify.OwningProcess -gt 0) {
    Write-Host "[WARN] Port $Port is still in use by PID $($verify.OwningProcess)." -ForegroundColor Yellow
} else {
    Write-Host "[PASS] Port $Port released successfully." -ForegroundColor Green
    Write-Host "[PASS] KubeCostFinOps backend stopped cleanly." -ForegroundColor Green
}

Write-Host ""
Write-Host "===========================================================================" -ForegroundColor Cyan
Write-Host ""

