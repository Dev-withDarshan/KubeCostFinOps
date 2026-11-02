# ==============================================================================
# STOP_PRESENTATION.ps1 — Graceful Shutdown for Presentation Mode
# KubeCostFinOps: Kubernetes Cost Optimization Framework (BCSE355L)
# Institution: VIT Vellore | Project Lead: K. Darshan
# ==============================================================================

[CmdletBinding()]
param(
    [int]$Port = 8000
)

$ErrorActionPreference = 'SilentlyContinue'

Write-Host ''
Write-Host '===========================================================================' -ForegroundColor Cyan
Write-Host '  STOPPING KUBECOST FINOPS PRESENTATION SERVICES' -ForegroundColor Cyan
Write-Host '===========================================================================' -ForegroundColor Cyan
Write-Host ''

$pidFile = '.backend.pid'

# 1. Stop by recorded PID
if (Test-Path $pidFile) {
    try {
        $savedPid = Get-Content $pidFile | ForEach-Object { [int]$_ }
        if ($savedPid -gt 0) {
            $p = Get-Process -Id $savedPid -ErrorAction SilentlyContinue
            if ($p) {
                Write-Host ('[INFO] Stopping backend process (PID: ' + $savedPid + ')...') -ForegroundColor Cyan
                Stop-Process -Id $savedPid -Force -ErrorAction SilentlyContinue
            }
        }
    } catch {}
    Remove-Item -Path $pidFile -Force -ErrorAction SilentlyContinue
}

# 2. Free port 8000
$conns = Get-NetTCPConnection -LocalPort $Port -State Listen -ErrorAction SilentlyContinue
if ($conns) {
    foreach ($conn in $conns) {
        $owningPid = $conn.OwningProcess
        if ($owningPid -gt 0) {
            $p = Get-Process -Id $owningPid -ErrorAction SilentlyContinue
            if ($p -and $p.ProcessName -match 'python') {
                Write-Host ('[INFO] Terminating lingering process on port ' + $Port + ' (PID ' + $owningPid + ')...') -ForegroundColor Cyan
                Stop-Process -Id $owningPid -Force -ErrorAction SilentlyContinue
            }
        }
    }
}

Start-Sleep -Milliseconds 600

# 3. Verification
$verify = Get-NetTCPConnection -LocalPort $Port -State Listen -ErrorAction SilentlyContinue
if ($verify -and $verify.OwningProcess -gt 0) {
    Write-Host ('[WARN] Port ' + $Port + ' still held by PID ' + $verify.OwningProcess) -ForegroundColor Yellow
} else {
    Write-Host '[PASS] Presentation services stopped. Port 8000 released.' -ForegroundColor Green
}

Write-Host ''
Write-Host '===========================================================================' -ForegroundColor Cyan
Write-Host ''
