# scripts/verify_monitoring.ps1 — KubeCostFinOps Monitoring Infrastructure Verification Script
# Validates namespaces, pods, services, Prometheus targets, KSM metrics, and OpenCost allocation API.
# Produces timestamped verification evidence under results/stage_06/.

[CmdletBinding()]
param(
    [string]$ClusterContext = "kind-kubecost-finops-local",
    [string]$OutputDir = "results/stage_06",
    [switch]$Detailed = $false
)

$ErrorActionPreference = "Continue"

function Write-Step {
    param([string]$Message)
    Write-Host "`n===========================================================================" -ForegroundColor Cyan
    Write-Host ">> $Message" -ForegroundColor Cyan
    Write-Host "===========================================================================" -ForegroundColor Cyan
}

function Write-Success {
    param([string]$Message)
    Write-Host "[PASS] $Message" -ForegroundColor Green
}

function Write-WarnMsg {
    param([string]$Message)
    Write-Host "[WARN] $Message" -ForegroundColor Yellow
}

function Write-Fail {
    param([string]$Message)
    Write-Host "[FAIL] $Message" -ForegroundColor Red
}

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$ProjectRoot = Split-Path -Parent $ScriptDir
Set-Location -Path $ProjectRoot

$Timestamp = (Get-Date).ToString("yyyyMMdd_HHmmss")
$FullOutputDir = Join-Path $ProjectRoot $OutputDir
if (-not (Test-Path $FullOutputDir)) {
    New-Item -ItemType Directory -Path $FullOutputDir -Force | Out-Null
}

$LogFile = Join-Path $FullOutputDir "stage_06_verification_${Timestamp}.log"
$JsonReportFile = Join-Path $FullOutputDir "stage_06_verification_${Timestamp}.json"

$Report = [ordered]@{
    timestamp = (Get-Date).ToString("o")
    stage = "stage_06_monitoring_setup"
    cluster_context = $ClusterContext
    checks = @{}
    summary = @{ total = 0; passed = 0; failed = 0; warnings = 0 }
}

function Record-Check {
    param([string]$Name, [string]$Status, [string]$Details)
    $Report.checks[$Name] = @{ status = $Status; details = $Details }
    $Report.summary.total++
    if ($Status -eq "PASS") { $Report.summary.passed++ }
    elseif ($Status -eq "WARN") { $Report.summary.warnings++ }
    else { $Report.summary.failed++ }
}

"===========================================================================" | Out-File -FilePath $LogFile
"KUBECOSTFINOPS STAGE 06 MONITORING VERIFICATION LOG - $Timestamp" | Out-File -FilePath $LogFile -Append
"===========================================================================" | Out-File -FilePath $LogFile -Append

Write-Step "1. Checking Cluster Reachability"
$ClusterInfo = & kubectl cluster-info --context $ClusterContext 2>&1
if ($LASTEXITCODE -eq 0) {
    Write-Success "Cluster '$ClusterContext' is reachable."
    Record-Check "cluster_reachability" "PASS" "Kubernetes control plane is reachable."
    $ClusterInfo | Out-File -FilePath $LogFile -Append
} else {
    Write-Fail "Cluster '$ClusterContext' is unreachable. Ensure Docker and Kind are running."
    Record-Check "cluster_reachability" "FAIL" "Cannot connect to cluster context '$ClusterContext': $ClusterInfo"
    $ClusterInfo | Out-File -FilePath $LogFile -Append
    
    # Save partial report and exit
    $Report | ConvertTo-Json -Depth 5 | Out-File -FilePath $JsonReportFile -Encoding UTF8
    Write-Host "`nVerification stopped: cluster unreachable. Log saved to: $LogFile" -ForegroundColor Yellow
    exit 1
}

Write-Step "2. Verifying Dedicated Namespaces"
$Namespaces = & kubectl get namespaces -o jsonpath='{.items[*].metadata.name}' 2>&1
$NsList = $Namespaces -split " "
if ($NsList -contains "monitoring" -and $NsList -contains "edusaas") {
    Write-Success "Namespaces 'monitoring' and 'edusaas' exist."
    Record-Check "namespaces" "PASS" "Namespaces 'monitoring' and 'edusaas' are active."
} else {
    Write-Fail "Missing required namespaces. Found: $Namespaces"
    Record-Check "namespaces" "FAIL" "Namespaces missing: monitoring in list: $($NsList -contains 'monitoring'); edusaas: $($NsList -contains 'edusaas')"
}

Write-Step "3. Verifying Pod Readiness in 'monitoring' Namespace"
$MonPodsJson = & kubectl get pods -n monitoring -o json 2>&1 | ConvertFrom-Json -ErrorAction SilentlyContinue
if ($MonPodsJson -and $MonPodsJson.items) {
    $AllReady = $true
    foreach ($pod in $MonPodsJson.items) {
        $pName = $pod.metadata.name
        $phase = $pod.status.phase
        $ready = ($pod.status.containerStatuses | Where-Object { $_.ready -eq $true }).Count
        $total = ($pod.status.containerStatuses).Count
        Write-Host "  Pod: $pName | Phase: $phase | Ready: $ready/$total"
        if ($phase -ne "Running" -or $ready -lt $total) {
            $AllReady = $false
        }
    }
    if ($AllReady) {
        Write-Success "All monitoring pods are Running and Ready."
        Record-Check "monitoring_pods" "PASS" "$($MonPodsJson.items.Count) pods active and ready."
    } else {
        Write-WarnMsg "Some monitoring pods are not fully ready."
        Record-Check "monitoring_pods" "WARN" "One or more pods not ready in namespace monitoring."
    }
} else {
    Write-Fail "No pods found in 'monitoring' namespace."
    Record-Check "monitoring_pods" "FAIL" "No pods returned from kubectl get pods -n monitoring."
}

Write-Step "4. Verifying ClusterIP Services in 'monitoring' Namespace"
$Services = & kubectl get svc -n monitoring -o jsonpath='{.items[*].metadata.name}' 2>&1
$SvcList = $Services -split " "
$ExpectedSvcs = @("kube-state-metrics", "prometheus-server", "opencost")
$MissingSvcs = @()
foreach ($s in $ExpectedSvcs) {
    if ($SvcList -contains $s) {
        Write-Success "Service '$s' found."
    } else {
        Write-Fail "Service '$s' is missing."
        $MissingSvcs += $s
    }
}
if ($MissingSvcs.Count -eq 0) {
    Record-Check "monitoring_services" "PASS" "All required services (KSM, Prometheus, OpenCost) present."
} else {
    Record-Check "monitoring_services" "FAIL" "Missing services: $($MissingSvcs -join ', ')"
}

Write-Step "5. Testing Kube-State-Metrics Telemetry Exposition"
$KsmPod = & kubectl get pod -n monitoring -l app.kubernetes.io/name=kube-state-metrics -o jsonpath='{.items[0].metadata.name}' 2>&1
if ($KsmPod -and -not ($KsmPod -like "*Error*")) {
    $KsmSample = & kubectl exec -n monitoring $KsmPod -c kube-state-metrics -- wget -qO- http://localhost:8080/metrics 2>&1
    if ($KsmSample -like "*kube_pod_info*" -and $KsmSample -like "*kube_pod_container_resource_requests*") {
        Write-Success "KSM metrics successfully verified: found 'kube_pod_info' and 'kube_pod_container_resource_requests'."
        Record-Check "ksm_metrics" "PASS" "Object-state metrics validated from port 8080."
    } else {
        Write-WarnMsg "KSM responded, but expected metric keys were not detected in initial output."
        Record-Check "ksm_metrics" "WARN" "KSM responded but key metrics missing."
    }
} else {
    Write-Fail "Could not target kube-state-metrics pod for metric probe."
    Record-Check "ksm_metrics" "FAIL" "KSM pod not found."
}

Write-Step "6. Testing Prometheus Scrape Target Health"
$PromPod = & kubectl get pod -n monitoring -l app.kubernetes.io/name=prometheus-server -o jsonpath='{.items[0].metadata.name}' 2>&1
if ($PromPod -and -not ($PromPod -like "*Error*")) {
    $TargetsJson = & kubectl exec -n monitoring $PromPod -c prometheus -- wget -qO- http://localhost:9090/api/v1/targets 2>&1 | ConvertFrom-Json -ErrorAction SilentlyContinue
    if ($TargetsJson -and $TargetsJson.status -eq "success") {
        $ActiveTargets = $TargetsJson.data.activeTargets
        Write-Host "  Discovered $($ActiveTargets.Count) active Prometheus scrape targets."
        $HealthyTargets = ($ActiveTargets | Where-Object { $_.health -eq "up" }).Count
        Write-Host "  Healthy (UP) targets: $HealthyTargets / $($ActiveTargets.Count)"
        foreach ($t in $ActiveTargets) {
            Write-Host "    Job: $($t.labels.job) | Target: $($t.discoveredLabels.__address__) | Health: $($t.health)"
        }
        if ($HealthyTargets -gt 0) {
            Write-Success "Prometheus scrape targets verified operational ($HealthyTargets targets UP)."
            Record-Check "prometheus_targets" "PASS" "$HealthyTargets targets in UP state."
        } else {
            Write-WarnMsg "Prometheus targets discovered, but none currently report health=up."
            Record-Check "prometheus_targets" "WARN" "Targets discovered but health not UP yet."
        }
    } else {
        Write-WarnMsg "Prometheus did not return valid targets JSON on /api/v1/targets."
        Record-Check "prometheus_targets" "WARN" "Could not parse /api/v1/targets response."
    }
} else {
    Write-Fail "Could not target prometheus-server pod for API probe."
    Record-Check "prometheus_targets" "FAIL" "Prometheus pod not found."
}

Write-Step "7. Testing OpenCost Allocation Compute API"
$OcPod = & kubectl get pod -n monitoring -l app.kubernetes.io/name=opencost -o jsonpath='{.items[0].metadata.name}' 2>&1
if ($OcPod -and -not ($OcPod -like "*Error*")) {
    $OcAllocJson = & kubectl exec -n monitoring $OcPod -c opencost -- wget -qO- "http://localhost:9003/allocation/compute?window=1h" 2>&1 | ConvertFrom-Json -ErrorAction SilentlyContinue
    if ($OcAllocJson -and ($OcAllocJson.code -eq 200 -or $OcAllocJson.data)) {
        Write-Success "OpenCost allocation compute API responded with HTTP 200 / valid data payload."
        Record-Check "opencost_allocation_api" "PASS" "OpenCost allocation/compute returned valid response."
    } else {
        Write-WarnMsg "OpenCost responded, but payload format requires inspection."
        Record-Check "opencost_allocation_api" "WARN" "OpenCost responded with non-standard payload or initialization state."
    }
} else {
    Write-Fail "Could not target opencost pod for API probe."
    Record-Check "opencost_allocation_api" "FAIL" "OpenCost pod not found."
}

Write-Step "8. Verification Summary and Report Generation"
$Report | ConvertTo-Json -Depth 6 | Out-File -FilePath $JsonReportFile -Encoding UTF8
Write-Host "`nSummary:"
Write-Host "  Total Checks: $($Report.summary.total)"
Write-Host "  Passed:       $($Report.summary.passed)" -ForegroundColor Green
Write-Host "  Warnings:     $($Report.summary.warnings)" -ForegroundColor Yellow
Write-Host "  Failed:       $($Report.summary.failed)" -ForegroundColor Red
Write-Host "`nEvidence saved to:"
Write-Host "  JSON: $JsonReportFile"
Write-Host "  LOG:  $LogFile"
