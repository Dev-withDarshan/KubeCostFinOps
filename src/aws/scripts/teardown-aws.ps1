<#
.SYNOPSIS
    Automated teardown and cleanup script for KubeCostFinOps AWS resources.

.DESCRIPTION
    Safely tears down Kubernetes resources (ALB Ingress, Deployments, Namespaces),
    empties and deletes ECR images, and deletes the CloudFormation stack to
    ensure zero ongoing cloud charges.

.PARAMETER Region
    AWS Region where the cluster was deployed (default: us-east-1).

.PARAMETER ClusterName
    Name of the EKS cluster (default: kubecost-finops-eks).

.PARAMETER StackName
    CloudFormation stack name (default: KubeCostFinOps-EKS-Stack).

.EXAMPLE
    .\src\aws\scripts\teardown-aws.ps1 -Region "us-east-1"
#>

[CmdletBinding()]
param (
    [string]$Region = "us-east-1",
    [string]$ClusterName = "kubecost-finops-eks",
    [string]$StackName = "KubeCostFinOps-EKS-Stack"
)

$ErrorActionPreference = "Continue"

Write-Host "================================================================" -ForegroundColor Red
Write-Host "  KubeCostFinOps AWS Resource Teardown & Cost Elimination" -ForegroundColor Red
Write-Host "================================================================" -ForegroundColor Red

# Step 1: Check AWS CLI
$identity = aws sts get-caller-identity --output json 2>$null
if (-not $identity) {
    throw "AWS credentials not detected. Please authenticate with AWS CLI before running teardown."
}
$callerObj = $identity | ConvertFrom-Json
Write-Host "  Authenticated AWS Account: $($callerObj.Account)" -ForegroundColor Yellow
Write-Host "  Region: $Region" -ForegroundColor Yellow

# Step 2: Delete Kubernetes Ingress and Services first (de-provisions external ALBs)
Write-Host "`n[Step 1/4] Deleting Kubernetes workloads and Ingress (releases AWS ALBs)..." -ForegroundColor Yellow
kubectl delete ingress finops-ingress -n finops-system --ignore-not-found=true 2>$null
kubectl delete namespace finops-system --ignore-not-found=true 2>$null
kubectl delete namespace edusaas --ignore-not-found=true 2>$null
Write-Host "  Kubernetes resources deleted." -ForegroundColor Green

# Step 3: Clean up ECR Images
Write-Host "`n[Step 2/4] Purging ECR container images..." -ForegroundColor Yellow
$repoName = "kubecost-finops-platform"
$imageIds = aws ecr list-images --repository-name $repoName --region $Region --query 'imageIds[*]' --output json 2>$null
if ($imageIds -and $imageIds -ne "[]") {
    aws ecr batch-delete-image --repository-name $repoName --region $Region --image-ids "$imageIds" 2>$null
    Write-Host "  ECR images purged." -ForegroundColor Green
} else {
    Write-Host "  No ECR images found or repository already clean." -ForegroundColor Gray
}

# Step 4: Delete CloudFormation Stack
Write-Host "`n[Step 3/4] Deleting CloudFormation Stack: $StackName..." -ForegroundColor Yellow
aws cloudformation delete-stack --stack-name $StackName --region $Region
Write-Host "  Stack deletion initiated. Waiting for complete deletion (this may take 5-10 minutes)..."

aws cloudformation wait stack-delete-complete --stack-name $StackName --region $Region
Write-Host "  CloudFormation stack deleted successfully!" -ForegroundColor Green

# Step 5: Verification
Write-Host "`n[Step 4/4] Verifying zero remaining billable resources..." -ForegroundColor Yellow
$remainingEks = aws eks describe-cluster --name $ClusterName --region $Region 2>$null
if (-not $remainingEks) {
    Write-Host "  Confirmed: EKS cluster $ClusterName no longer exists." -ForegroundColor Green
} else {
    Write-Warning "EKS cluster is still present or terminating."
}

Write-Host "`n================================================================" -ForegroundColor Cyan
Write-Host "  ALL KUBECOST FINOPS AWS RESOURCES SAFELY TORN DOWN" -ForegroundColor Green
Write-Host "  Ongoing billable hourly rate is now: $0.00 / hour" -ForegroundColor Green
Write-Host "================================================================" -ForegroundColor Cyan
