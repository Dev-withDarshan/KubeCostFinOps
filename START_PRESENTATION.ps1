# ==============================================================================
# START_PRESENTATION.ps1 — Guaranteed Presentation Startup System
# KubeCostFinOps: Kubernetes Cost Optimization Framework (BCSE355L)
# Institution: VIT Vellore |
# ==============================================================================

[CmdletBinding()]
param(
    [int]$Port = 8000,
    [string]$HostAddress = '127.0.0.1',
    [switch]$NoBrowser
)

$ErrorActionPreference = 'Stop'

Write-Host ''
Write-Host '===========================================================================' -ForegroundColor Cyan
Write-Host '  KUBECOST FINOPS -- LIVE PRESENTATION MODE (BCSE355L EVALUATION)' -ForegroundColor Cyan
Write-Host '  Department of Cloud Architecture | VIT Vellore |' -ForegroundColor Cyan
Write-Host '===========================================================================' -ForegroundColor Cyan
Write-Host ''

# 1. Project Directory Verification
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
if ($scriptDir) { Set-Location $scriptDir }

$requiredFiles = @(
    'src/backend/main.py',
    'src/frontend/index.html',
    'src/frontend/app.js',
    'src/frontend/styles.css',
    'src/finops_engine/kubecost_config.yaml'
)

foreach ($f in $requiredFiles) {
    if (-not (Test-Path $f)) {
        Write-Host ('[FAIL] Missing required project file: ' + $f) -ForegroundColor Red
        exit 1
    }
}
Write-Host ('[PASS] Workspace root verified: ' + $PWD) -ForegroundColor Green

# 2. Check Python Runtime
$pythonCmd = 'python'
try {
    $pythonVer = python --version 2>&1
    Write-Host ('[PASS] Python environment verified: ' + $pythonVer) -ForegroundColor Green
    $pythonPath = (Get-Command python -ErrorAction SilentlyContinue).Source
    if ($pythonPath) {
        $pythonwPath = $pythonPath -replace 'python\.exe$', 'pythonw.exe'
        if (Test-Path $pythonwPath) {
            $pythonCmd = $pythonwPath
        }
    }
}
catch {
    Write-Host '[FAIL] Python runtime not found in PATH.' -ForegroundColor Red
    exit 1
}

# 3. Port & Readiness Check
$targetUrl = 'http://' + $HostAddress + ':' + $Port
$readyUrl = $targetUrl + '/api/ready'
$alreadyRunning = $false

try {
    $existingResp = Invoke-RestMethod -Uri $readyUrl -TimeoutSec 1 -ErrorAction Stop
    if ($existingResp.status -eq 'READY') {
        Write-Host ('[PASS] KubeCostFinOps backend is already active on port ' + $Port + '.') -ForegroundColor Green
        $alreadyRunning = $true
    }
}
catch {
    # Port not answering, start fresh
}

if (-not $alreadyRunning) {
    # 3a. Clean up any previous backend process from PID file
    if (Test-Path '.backend.pid') {
        try {
            $prevPid = Get-Content '.backend.pid' | ForEach-Object { [int]$_ }
            if ($prevPid -gt 0) {
                $p = Get-Process -Id $prevPid -ErrorAction SilentlyContinue
                if ($p -and $p.ProcessName -match 'python') {
                    Write-Host ('[INFO] Stopping previously recorded backend PID ' + $prevPid + '...') -ForegroundColor Yellow
                    Stop-Process -Id $prevPid -Force -ErrorAction SilentlyContinue
                    Start-Sleep -Milliseconds 500
                }
            }
        } catch {}
        Remove-Item -Path '.backend.pid' -Force -ErrorAction SilentlyContinue
    }

    # 3b. Clear any stale connection on port 8000
    $stale = Get-NetTCPConnection -LocalPort $Port -State Listen -ErrorAction SilentlyContinue
    if ($stale -and $stale.OwningProcess -gt 0) {
        Write-Host ('[INFO] Releasing port ' + $Port + ' from PID ' + $stale.OwningProcess + '...') -ForegroundColor Yellow
        Stop-Process -Id $stale.OwningProcess -Force -ErrorAction SilentlyContinue
        Start-Sleep -Seconds 1
    }

    Write-Host ('[INFO] Launching presentation backend server on port ' + $Port + ' with ' + (Split-Path $pythonCmd -Leaf) + '...') -ForegroundColor Cyan
    $backendCmd = '-m src.backend.main --port ' + $Port + ' --host ' + $HostAddress
    $proc = Start-Process -FilePath $pythonCmd -ArgumentList $backendCmd -WorkingDirectory $scriptDir -WindowStyle Hidden -PassThru

    if (-not $proc) {
        Write-Host '[FAIL] Could not spawn backend process.' -ForegroundColor Red
        exit 1
    }

    $proc.Id | Out-File -FilePath '.backend.pid' -Encoding ascii -Force
    Write-Host ('[PASS] Backend process started (PID: ' + $proc.Id + ')') -ForegroundColor Green

    # Wait for readiness
    Write-Host '[INFO] Verifying backend readiness...' -NoNewline
    $ready = $false
    for ($i = 0; $i -lt 15; $i++) {
        Start-Sleep -Milliseconds 400
        Write-Host '.' -NoNewline
        try {
            $checkResp = Invoke-RestMethod -Uri $readyUrl -TimeoutSec 1 -ErrorAction SilentlyContinue
            if ($checkResp.status -eq 'READY') {
                $ready = $true
                break
            }
        }
        catch {}
    }
    Write-Host ''

    if (-not $ready) {
        Write-Host '[FAIL] Backend did not respond within timeout.' -ForegroundColor Red
        exit 1
    }
}

Write-Host '[PASS] Backend status verified: HTTP 200 READY' -ForegroundColor Green

# 4. Launch Browser
if (-not $NoBrowser) {
    Write-Host '[INFO] Opening FinOps Dashboard in web browser...' -ForegroundColor Cyan
    Start-Process $targetUrl
}

# 5. Output Presentation Cheatsheet
Write-Host ''
Write-Host '===========================================================================' -ForegroundColor Green
Write-Host '  DEMONSTRATION COCKPIT IS LIVE FOR FACULTY EVALUATION' -ForegroundColor Green
Write-Host '===========================================================================' -ForegroundColor Green
Write-Host ''
Write-Host ('  Live Dashboard URL     : ' + $targetUrl) -ForegroundColor Cyan
Write-Host ('  API Health Endpoint    : ' + $targetUrl + '/api/health') -ForegroundColor White
Write-Host ('  API Readiness Endpoint : ' + $targetUrl + '/api/ready') -ForegroundColor White
Write-Host ('  Monitoring Telemetry   : ' + $targetUrl + '/api/v1/monitoring/status') -ForegroundColor White
Write-Host ('  Modeled Cost Summary   : ' + $targetUrl + '/api/v1/costs/summary') -ForegroundColor White
Write-Host ('  FinOps Recommendations : ' + $targetUrl + '/api/v1/recommendations') -ForegroundColor White
Write-Host ('  Forensic Experiments  : ' + $targetUrl + '/api/v1/experiments') -ForegroundColor White
Write-Host ('  Workload Demand Model  : ' + $targetUrl + '/api/v1/forecast?source=synthetic') -ForegroundColor White
Write-Host ''
Write-Host '  DEMONSTRATION TALKING POINTS:' -ForegroundColor Yellow
Write-Host '  1. Executive KPI Cards: $24.15 baseline spend down to $7.48 rightsized (69% savings).' -ForegroundColor Gray
Write-Host '  2. Rightsizing Logic: 20% safety headroom over peak cgroups utilization with minimum floor.' -ForegroundColor Gray
Write-Host '  3. Controlled Experiment: 4-phase benchmark (exp-20261016-141448) with 10/10 forensic validation.' -ForegroundColor Gray
Write-Host '  4. Forecasting: Holt Linear Trend baseline model with 95% confidence intervals.' -ForegroundColor Gray
Write-Host '  5. Strict Provenance: Explicit separation of measured telemetry vs modeled rates.' -ForegroundColor Gray
Write-Host ''
Write-Host '  To cleanly stop the presentation demo afterwards:' -ForegroundColor Yellow
Write-Host '    .\STOP_PRESENTATION.ps1' -ForegroundColor Yellow
Write-Host ''
Write-Host '===========================================================================' -ForegroundColor Green
Write-Host ''

