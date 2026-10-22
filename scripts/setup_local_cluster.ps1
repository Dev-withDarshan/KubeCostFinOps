# scripts/setup_local_cluster.ps1 — KubeCostFinOps Local Cluster Setup Script
# Reproducible provisioning and deployment of local Kind cluster and monitoring stack.
# Target: Windows PowerShell 5.1+ / PowerShell Core 7+

[CmdletBinding()]
param(
    [string]$ClusterName = "kubecost-finops-local",
    [string]$ConfigFile = "kind-config.yaml",
    [switch]$SkipWorkload = $false,
    [switch]$DryRun = $false
)

$ErrorActionPreference = "Stop"

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

Write-Step "1. Inspecting Host Tooling and Hardware Prerequisites"

# 1.1 Check Git
if (Get-Command git -ErrorAction SilentlyContinue) {
    Write-Success "Git available: $((git --version).Trim())"
} else {
    Write-WarnMsg "Git CLI not found in PATH."
}

# 1.2 Check Python
if (Get-Command python -ErrorAction SilentlyContinue) {
    Write-Success "Python available: $((python --version).Trim())"
} else {
    Write-WarnMsg "Python CLI not found in PATH."
}

# 1.3 Check Docker
$DockerCmd = Get-Command docker -ErrorAction SilentlyContinue
if (-not $DockerCmd) {
    Write-Fail "Docker CLI ('docker') not found in PATH. Please install Docker Desktop."
    if (-not $DryRun) { exit 1 }
} else {
    Write-Success "Docker CLI found: $($DockerCmd.Source)"
}

# Check if Docker Daemon is running
$DockerRunning = $false
try {
    $null = docker info 2>&1
    if ($LASTEXITCODE -eq 0) {
        $DockerRunning = $true
        Write-Success "Docker Engine daemon is running and responsive."
    }
} catch {}

if (-not $DockerRunning) {
    if ($DryRun) {
        Write-WarnMsg "Docker daemon is NOT currently running (Dry-Run mode: continuing prerequisite check)."
    } else {
        Write-Fail "Docker daemon is NOT running or unreachable."
        Write-Host "`nDIAGNOSTIC & REMEDIATION:" -ForegroundColor Yellow
        Write-Host "  1. Launch Docker Desktop from the Start Menu, or execute:"
        Write-Host "     & 'C:\Program Files\Docker\Docker\Docker Desktop.exe' (or from AppData)"
        Write-Host "  2. Wait until the whale icon in the Windows notification tray indicates 'Engine running'."
        Write-Host "  3. Re-run this script once Docker Desktop is initialized."
        Write-Host "`nIf host resources are constrained, verify RAM requirements before launching."
        exit 1
    }
}

# 1.4 Check Kind CLI
$KindCmd = Get-Command kind -ErrorAction SilentlyContinue
if (-not $KindCmd) {
    Write-Fail "Kind CLI ('kind') not found in PATH. Please install Kind via winget: 'winget install Kubernetes.kind'"
    if (-not $DryRun) { exit 1 }
} else {
    Write-Success "Kind CLI found: $((kind version).Trim())"
}

# 1.5 Check kubectl CLI
$KubectlCmd = Get-Command kubectl -ErrorAction SilentlyContinue
if (-not $KubectlCmd) {
    Write-Fail "kubectl CLI ('kubectl') not found in PATH. Please install kubectl or enable it via Docker Desktop."
    if (-not $DryRun) { exit 1 }
} else {
    Write-Success "kubectl CLI found: Client Version v1.36.1+"
}

# 1.6 Check Host Memory
try {
    $os = Get-CimInstance Win32_OperatingSystem -ErrorAction SilentlyContinue
    if ($os) {
        $TotalRAM = [math]::Round($os.TotalVisibleMemorySize / 1MB, 2)
        $FreeRAM  = [math]::Round($os.FreePhysicalMemory / 1MB, 2)
        Write-Host "  Host Total RAM: ${TotalRAM} GB | Free RAM: ${FreeRAM} GB"
        if ($FreeRAM -lt 2.0) {
            Write-WarnMsg "Available physical memory is low (< 2.0 GB). Kind cluster is configured in single-node lean mode to conserve RAM."
        } else {
            Write-Success "Host physical memory headroom is adequate (${FreeRAM} GB free)."
        }
    }
} catch {}

if ($DryRun) {
    Write-Host "`n[DRY-RUN COMPLETE] All prerequisite checks evaluated." -ForegroundColor Green
    if (-not $DockerRunning) {
        Write-WarnMsg "To deploy the cluster live, please start Docker Desktop first."
    } else {
        Write-Success "Environment is ready for live cluster deployment."
    }
    exit 0
}

Write-Step "2. Verifying or Creating Kind Cluster: $ClusterName"

$ExistingClusters = & kind get clusters 2>&1
if ($ExistingClusters -contains $ClusterName) {
    Write-Success "Kind cluster '$ClusterName' already exists. Preserving existing cluster."
} else {
    if (-not (Test-Path $ConfigFile)) {
        Write-Fail "Cluster config file '$ConfigFile' not found at '$ProjectRoot\$ConfigFile'."
        exit 1
    }
    Write-Host "Creating Kind cluster '$ClusterName' using '$ConfigFile'..." -ForegroundColor Cyan
    & kind create cluster --name $ClusterName --config $ConfigFile
    if ($LASTEXITCODE -ne 0) {
        Write-Fail "Failed to create Kind cluster '$ClusterName'."
        exit 1
    }
    Write-Success "Kind cluster '$ClusterName' created successfully."
}

# Ensure context is active
& kubectl config use-context "kind-$ClusterName" | Out-Null
Write-Success "kubectl context set to: kind-$ClusterName"

Write-Step "3. Applying Namespaces and Workload Quotas"
& kubectl apply -f src/k8s/namespace.yaml
if ($LASTEXITCODE -ne 0) {
    Write-Fail "Failed to apply src/k8s/namespace.yaml."
    exit 1
}
Write-Success "Namespaces 'monitoring' and 'edusaas' applied."

Write-Step "4. Deploying Kube-State-Metrics (KSM v2.12.0)"
& kubectl apply -f src/k8s/monitoring/ksm.yaml
Write-Host "Waiting for kube-state-metrics rollout..."
& kubectl rollout status deployment/kube-state-metrics -n monitoring --timeout=120s
if ($LASTEXITCODE -ne 0) {
    Write-Fail "Kube-state-metrics deployment rollout timed out or failed."
    Write-Host "Diagnostic: kubectl describe pod -l app.kubernetes.io/name=kube-state-metrics -n monitoring"
    exit 1
}
Write-Success "Kube-state-metrics is Ready."

Write-Step "5. Deploying Prometheus Server (v2.51.0)"
& kubectl apply -f src/k8s/monitoring/prometheus.yaml
Write-Host "Waiting for prometheus-server rollout..."
& kubectl rollout status deployment/prometheus-server -n monitoring --timeout=120s
if ($LASTEXITCODE -ne 0) {
    Write-Fail "Prometheus server deployment rollout timed out or failed."
    Write-Host "Diagnostic: kubectl describe pod -l app.kubernetes.io/name=prometheus-server -n monitoring"
    exit 1
}
Write-Success "Prometheus server is Ready."

Write-Step "6. Deploying OpenCost Cost Allocation Engine (v1.108.1)"
& kubectl apply -f src/k8s/monitoring/opencost.yaml
Write-Host "Waiting for opencost rollout..."
& kubectl rollout status deployment/opencost -n monitoring --timeout=180s
if ($LASTEXITCODE -ne 0) {
    Write-Fail "OpenCost deployment rollout timed out or failed."
    Write-Host "Diagnostic: kubectl describe pod -l app.kubernetes.io/name=opencost -n monitoring"
    exit 1
}
Write-Success "OpenCost allocation engine is Ready."

if (-not $SkipWorkload) {
    Write-Step "7. Deploying EduSaaS Baseline Workload"
    & kubectl apply -f src/k8s/deployment.yaml
    & kubectl apply -f src/k8s/service.yaml
    & kubectl apply -f src/k8s/hpa.yaml
    Write-Host "Waiting for edusaas-backend rollout..."
    & kubectl rollout status deployment/edusaas-backend -n edusaas --timeout=120s
    if ($LASTEXITCODE -eq 0) {
        Write-Success "EduSaaS backend workload is Ready."
    } else {
        Write-WarnMsg "Workload rollout taking longer than expected. Check: kubectl get pods -n edusaas"
    }
}

Write-Step "8. Cluster Deployment Summary"
Write-Host "`nPod Status across Namespaces:" -ForegroundColor Green
& kubectl get pods -n monitoring
Write-Host ""
& kubectl get pods -n edusaas

Write-Host "`nServices and ClusterIP Endpoints:" -ForegroundColor Green
& kubectl get svc -n monitoring
Write-Host ""
& kubectl get svc -n edusaas

Write-Host "`n===========================================================================" -ForegroundColor Cyan
Write-Host ">> MONITORING INFRASTRUCTURE SETUP COMPLETE!" -ForegroundColor Green
Write-Host "===========================================================================" -ForegroundColor Cyan
Write-Host "Next Steps:"
Write-Host "  1. Run verification script: powershell scripts/verify_monitoring.ps1"
Write-Host "  2. Port forward Prometheus: kubectl port-forward svc/prometheus-server -n monitoring 9090:9090"
Write-Host "  3. Port forward OpenCost:   kubectl port-forward svc/opencost -n monitoring 9003:9003"
Write-Host "  4. Query OpenCost API:      curl http://localhost:9003/allocation/compute"
Write-Host ""
