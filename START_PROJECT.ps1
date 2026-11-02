# ==============================================================================
# START_PROJECT.ps1 — Reliable One-Command Startup System
# KubeCostFinOps: Kubernetes Cost Optimization Framework (BCSE355L)
# Institution: VIT Vellore | Team Lead: K. Darshan
# Operating System: Windows 11 PowerShell
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
Write-Host '  KUBECOST FINOPS -- ONE-COMMAND STARTUP SYSTEM (WINDOWS 11)' -ForegroundColor Cyan
Write-Host '  BCSE355L Final Evaluation | VIT Vellore | Team Lead: K. Darshan' -ForegroundColor Cyan
Write-Host '===========================================================================' -ForegroundColor Cyan
Write-Host ''

# 1. Verify Project Directory
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
        Write-Host 'Please execute START_PROJECT.ps1 from the KubeCostFinOps root directory.' -ForegroundColor Yellow
        exit 1
    }
}
Write-Host ('[PASS] Project root verified: ' + $PWD) -ForegroundColor Green

# 2. Verify Python Runtime & Dependencies
try {
    $pythonVer = python --version 2>&1
    Write-Host ('[PASS] Python runtime detected: ' + $pythonVer) -ForegroundColor Green
} catch {
    Write-Host '[FAIL] Python was not found in PATH.' -ForegroundColor Red
    Write-Host 'Please install Python 3.10+ and add it to system PATH.' -ForegroundColor Yellow
    exit 1
}

# Verify dependencies
$depCheck = python -c "import yaml, pandas, numpy; print('DEPS_OK')" 2>&1
if ($depCheck -notmatch 'DEPS_OK') {
    Write-Host '[WARN] Some core packages are missing. Installing from requirements.txt...' -ForegroundColor Yellow
    pip install -r requirements.txt
} else {
    Write-Host '[PASS] Core Python dependencies verified (yaml, pandas, numpy)' -ForegroundColor Green
}

# 3. Check Port 8000 & Avoid Spawning Duplicate Processes
$targetUrl = 'http://' + $HostAddress + ':' + $Port
$readyUrl = $targetUrl + '/api/ready'
$alreadyRunning = $false

# First probe the endpoint directly: if it returns READY, it is already running
try {
    $existingResp = Invoke-RestMethod -Uri $readyUrl -TimeoutSec 1 -ErrorAction Stop
    if ($existingResp.status -eq 'READY') {
        Write-Host ('[PASS] KubeCostFinOps API is ALREADY running and healthy on port ' + $Port + ' (avoiding duplicate process).') -ForegroundColor Green
        $alreadyRunning = $true
    }
} catch {
    # Port is not currently responding to our ready endpoint
}

if (-not $alreadyRunning) {
    # Check if port is held by some dead or conflicting process
    $existingConns = Get-NetTCPConnection -LocalPort $Port -ErrorAction SilentlyContinue | Where-Object { $_.State -eq 'Listen' }
    if ($existingConns) {
        Write-Host ('[WARN] Port ' + $Port + ' is occupied by an unresponsive process. Attempting cleanup...') -ForegroundColor Yellow
        foreach ($conn in $existingConns) {
            if ($conn.OwningProcess -gt 0) {
                Stop-Process -Id $conn.OwningProcess -Force -ErrorAction SilentlyContinue
            }
        }
        Start-Sleep -Seconds 1
    }

    Write-Host ('[INFO] Starting lightweight FinOps REST backend server on port ' + $Port + '...') -ForegroundColor Cyan

    $backendCmd = '-m src.backend.main --port ' + $Port + ' --host ' + $HostAddress
    $proc = Start-Process -FilePath 'python' -ArgumentList $backendCmd -WorkingDirectory $scriptDir -WindowStyle Hidden -RedirectStandardOutput 'backend.log' -RedirectStandardError 'backend.err.log' -PassThru

    if (-not $proc) {
        Write-Host '[FAIL] Failed to launch backend process.' -ForegroundColor Red
        exit 1
    }

    # Record PID for clean teardown via STOP_PROJECT.ps1
    $proc.Id | Out-File -FilePath '.backend.pid' -Encoding ascii -Force
    Write-Host ('[PASS] Backend process launched (PID: ' + $proc.Id + ')') -ForegroundColor Green

    # Poll readiness endpoint up to 10 seconds
    Write-Host '[INFO] Awaiting backend readiness...' -NoNewline
    $ready = $false
    for ($i = 0; $i -lt 20; $i++) {
        Start-Sleep -Milliseconds 500
        Write-Host '.' -NoNewline
        try {
            $checkResp = Invoke-RestMethod -Uri $readyUrl -TimeoutSec 1 -ErrorAction SilentlyContinue
            if ($checkResp.status -eq 'READY') {
                $ready = $true
                break
            }
        } catch {
            # Continue polling
        }
    }
    Write-Host ''

    if (-not $ready) {
        Write-Host '[FAIL] Backend failed to report ready status within 10 seconds.' -ForegroundColor Red
        Write-Host ('Check if another application is blocking port ' + $Port) -ForegroundColor Yellow
        exit 1
    }
}

Write-Host '[PASS] Backend readiness confirmed: HTTP 200 READY' -ForegroundColor Green

# 5. Open Dashboard in Browser
if (-not $NoBrowser) {
    Write-Host '[INFO] Launching FinOps Dashboard in default web browser...' -ForegroundColor Cyan
    Start-Process $targetUrl
}

# 6. Print Endpoint Registry
Write-Host ''
Write-Host '===========================================================================' -ForegroundColor Green
Write-Host '  KUBECOST FINOPS PLATFORM IS LIVE AND READY FOR DEMO' -ForegroundColor Green
Write-Host '===========================================================================' -ForegroundColor Green
Write-Host ''
Write-Host ('  Interactive Dashboard  : ' + $targetUrl) -ForegroundColor Cyan
Write-Host ('  API Health Endpoint    : ' + $targetUrl + '/api/health') -ForegroundColor White
Write-Host ('  API Readiness Endpoint : ' + $targetUrl + '/api/ready') -ForegroundColor White
Write-Host ('  Monitoring Status      : ' + $targetUrl + '/api/v1/monitoring/status') -ForegroundColor White
Write-Host ('  Cost Intelligence      : ' + $targetUrl + '/api/v1/costs/summary') -ForegroundColor White
Write-Host ('  Rightsizing Guidance   : ' + $targetUrl + '/api/v1/recommendations') -ForegroundColor White
Write-Host ('  Benchmark Experiments  : ' + $targetUrl + '/api/v1/experiments') -ForegroundColor White
Write-Host ('  Demand Forecasting     : ' + $targetUrl + '/api/v1/forecast?source=synthetic') -ForegroundColor White
Write-Host ''
Write-Host '  To stop the running backend gracefully at any time, run:' -ForegroundColor Yellow
Write-Host '    .\STOP_PROJECT.ps1' -ForegroundColor Yellow
Write-Host ''
Write-Host '===========================================================================' -ForegroundColor Green
Write-Host ''
