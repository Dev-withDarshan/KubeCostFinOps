<#
.SYNOPSIS
    Automated deployment script for KubeCostFinOps on Amazon EKS.

.DESCRIPTION
    Provisions ultra-low-cost EKS cluster via CloudFormation, builds and pushes
    the FinOps container image to Amazon ECR, deploys Kubernetes workloads,
    and runs post-deployment health verification.

.PARAMETER Region
    AWS Region to deploy to (default: us-east-1).

.PARAMETER ClusterName
    Name of the EKS cluster (default: kubecost-finops-eks).

.PARAMETER StackName
    CloudFormation stack name (default: KubeCostFinOps-EKS-Stack).

.EXAMPLE
    .\src\aws\scripts\deploy-aws.ps1 -Region "us-east-1"
#>

[CmdletBinding()]
param (
    [string]$Region = "us-east-1",
    [string]$ClusterName = "kubecost-finops-eks",
    [string]$StackName = "KubeCostFinOps-EKS-Stack",
    [string]$NodeInstanceType = "t3.medium"
)

$ErrorActionPreference = "Stop"

Write-Host "================================================================" -ForegroundColor Cyan
Write-Host "  KubeCostFinOps AWS EKS Automated Deployment Pipeline" -ForegroundColor Cyan
Write-Host "================================================================" -ForegroundColor Cyan

# Step 1: Verify prerequisites
Write-Host "`n[Step 1/8] Verifying prerequisites..." -ForegroundColor Yellow

$awsCmd = Get-Command "aws" -ErrorAction SilentlyContinue
if (-not $awsCmd) {
    throw "AWS CLI not found on PATH. Please install AWS CLI v2."
}

$identity = aws sts get-caller-identity --output json 2>$null
if (-not $identity) {
    throw "AWS credentials not detected. Please run 'aws configure' or export AWS credentials before executing."
}
$callerObj = $identity | ConvertFrom-Json
Write-Host "  Authenticated AWS Account: $($callerObj.Account)" -ForegroundColor Green
Write-Host "  IAM Principal: $($callerObj.Arn)" -ForegroundColor Green
Write-Host "  Target Region: $Region" -ForegroundColor Green

$kubectlCmd = Get-Command "kubectl" -ErrorAction SilentlyContinue
if (-not $kubectlCmd) {
    Write-Warning "kubectl is not found on PATH. Manifest deployment will require kubectl."
}

$dockerCmd = Get-Command "docker" -ErrorAction SilentlyContinue
if (-not $dockerCmd) {
    Write-Warning "docker is not found on PATH. Image build/push will require Docker."
}

# Step 2: Deploy CloudFormation infrastructure
Write-Host "`n[Step 2/8] Provisioning AWS EKS Infrastructure via CloudFormation..." -ForegroundColor Yellow
$templatePath = Join-Path $PSScriptRoot "..\cloudformation\eks-infrastructure.yaml"

if (-not (Test-Path $templatePath)) {
    throw "CloudFormation template not found at: $templatePath"
}

Write-Host "  Deploying stack: $StackName (Cluster: $ClusterName, InstanceType: $NodeInstanceType)..."
aws cloudformation deploy `
    --template-file $templatePath `
    --stack-name $StackName `
    --parameter-overrides ClusterName=$ClusterName NodeInstanceType=$NodeInstanceType `
    --capabilities CAPABILITY_NAMED_IAM `
    --region $Region

Write-Host "  CloudFormation stack deployment complete!" -ForegroundColor Green

# Fetch outputs
$outputsJson = aws cloudformation describe-stacks --stack-name $StackName --region $Region --query "Stacks[0].Outputs" --output json | ConvertFrom-Json
$ecrRepoUri = ($outputsJson | Where-Object { $_.OutputKey -eq "ECRRepositoryUri" }).OutputValue
Write-Host "  ECR Repository URI: $ecrRepoUri" -ForegroundColor Green

# Step 3: Update local kubeconfig
Write-Host "`n[Step 3/8] Updating kubeconfig for EKS cluster..." -ForegroundColor Yellow
aws eks update-kubeconfig --name $ClusterName --region $Region
Write-Host "  Kubeconfig updated successfully." -ForegroundColor Green

# Step 4: Build and Push Docker image to ECR
Write-Host "`n[Step 4/8] Building and pushing Docker container to ECR..." -ForegroundColor Yellow
$imageTag = "v1.0.0"
$fullImage = "${ecrRepoUri}:${imageTag}"

Write-Host "  Authenticating Docker to Amazon ECR..."
aws ecr get-login-password --region $Region | docker login --username AWS --password-stdin $ecrRepoUri

$dockerfilePath = Join-Path $PSScriptRoot "..\Dockerfile"
$projectRoot = Resolve-Path (Join-Path $PSScriptRoot "..\..\..")

Write-Host "  Building image: $fullImage..."
docker build -t $fullImage -f $dockerfilePath $projectRoot

Write-Host "  Pushing image to ECR: $fullImage..."
docker push $fullImage
Write-Host "  Image pushed successfully." -ForegroundColor Green

# Step 5: Deploy Kubernetes manifests
Write-Host "`n[Step 5/8] Applying Kubernetes manifests..." -ForegroundColor Yellow
$k8sDir = Join-Path $PSScriptRoot "..\k8s"

kubectl apply -f (Join-Path $k8sDir "namespace.yaml")
kubectl apply -f (Join-Path $k8sDir "edusaas-workload.yaml")

# Render finops-platform.yaml with the real ECR image URI
$finopsManifest = Get-Content (Join-Path $k8sDir "finops-platform.yaml") -Raw
$finopsManifestRendered = $finopsManifest -replace "123456789012.dkr.ecr.us-east-1.amazonaws.com/kubecost-finops-platform:v1.0.0", $fullImage
$tempManifest = [System.IO.Path]::GetTempFileName() + ".yaml"
$finopsManifestRendered | Out-File -FilePath $tempManifest -Encoding utf8
kubectl apply -f $tempManifest
Remove-Item $tempManifest -Force

kubectl apply -f (Join-Path $k8sDir "hpa.yaml")
kubectl apply -f (Join-Path $k8sDir "ingress-alb.yaml")
Write-Host "  Kubernetes manifests applied." -ForegroundColor Green

# Step 6: Wait for deployment rollout
Write-Host "`n[Step 6/8] Waiting for workload rollouts..." -ForegroundColor Yellow
kubectl rollout status deployment/edusaas-lms -n edusaas --timeout=180s
kubectl rollout status deployment/finops-engine -n finops-system --timeout=180s
Write-Host "  All deployments are in ready state." -ForegroundColor Green

# Step 7: Post-deployment health verification
Write-Host "`n[Step 7/8] Running post-deployment health verification..." -ForegroundColor Yellow
Start-Sleep -Seconds 10

Write-Host "  Inspecting running Pods:"
kubectl get pods -n edusaas
kubectl get pods -n finops-system

Write-Host "  Inspecting Ingress endpoint:"
kubectl get ingress -n finops-system

# Step 8: Complete
Write-Host "`n================================================================" -ForegroundColor Cyan
Write-Host "  AWS EKS DEPLOYMENT COMPLETED SUCCESSFULLY!" -ForegroundColor Green
Write-Host "================================================================" -ForegroundColor Cyan
Write-Host "Cluster: $ClusterName | Region: $Region | Stack: $StackName"
Write-Host "To teardown and avoid ongoing charges, run:"
Write-Host "  .\src\aws\scripts\teardown-aws.ps1 -Region '$Region' -ClusterName '$ClusterName'" -ForegroundColor Yellow
