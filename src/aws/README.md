# KubeCostFinOps — AWS Production Deployment Architecture & Runbook

## 1. Architectural Overview

This directory provides the production-grade, highly secure, and cost-optimized deployment manifests for running the **Kubernetes Cost Optimization Framework for SaaS-Based Educational Platforms** on **Amazon Elastic Kubernetes Service (Amazon EKS)**.

```
+--------------------------------------------------------------------------------------------------+
|                                        AWS Cloud (us-east-1)                                     |
|                                                                                                  |
|   +------------------------------------------------------------------------------------------+   |
|   | Amazon Virtual Private Cloud (VPC: 10.0.0.0/16)                                          |   |
|   |                                                                                          |   |
|   |   +---------------------------------------+  +---------------------------------------+   |   |
|   |   | Public Subnet A (10.0.1.0/24)         |  | Public Subnet B (10.0.2.0/24)         |   |   |
|   |   | [Internet Gateway Attached]           |  | [Internet Gateway Attached]           |   |   |
|   |   |                                       |  |                                       |   |   |
|   |   |  +---------------------------------+  |  |  +---------------------------------+  |   |   |
|   |   |  | Application Load Balancer (ALB) |<-------+ Inbound HTTPS/HTTP (Port 80/443)    |  |   |
|   |   |  +----------------+----------------+  |  |  +---------------------------------+  |   |   |
|   |   |                   |                   |  |                                       |   |   |
|   |   |  +----------------v----------------+  |  |                                       |   |   |
|   |   |  | EKS Managed Node (t3.medium)    |  |  |                                       |   |   |
|   |   |  |                                 |  |  |                                       |   |   |
|   |   |  |  Namespace: finops-system       |  |  |                                       |   |   |
|   |   |  |  - finops-engine Deployment     |  |  |                                       |   |   |
|   |   |  |    (FastAPI + Vanilla JS UI)    |  |  |                                       |   |   |
|   |   |  |    (ServiceAccount: finops-sa)  |  |  |                                       |   |   |
|   |   |  |                                 |  |  |                                       |   |   |
|   |   |  |  Namespace: edusaas             |  |  |                                       |   |   |
|   |   |  |  - edusaas-lms Deployment       |  |  |                                       |   |   |
|   |   |  |    (2 Replicas, HPA 2-6)        |  |  |                                       |   |   |
|   |   |  +---------------------------------+  |  |                                       |   |   |
|   |   +---------------------------------------+  +---------------------------------------+   |   |
|   +------------------------------------------------------------------------------------------+   |
|                                                                                                  |
|   +------------------------------+             +---------------------------------------------+   |
|   | Amazon EKS Control Plane     |             | Amazon Elastic Container Registry (ECR)     |   |
|   | (Managed Kubernetes v1.31)   |             | (kubecost-finops-platform:v1.0.0)           |   |
|   +------------------------------+             +---------------------------------------------+   |
+--------------------------------------------------------------------------------------------------+
```

---

## 2. FinOps-Optimized Cost Architecture (Zero-NAT Gateway)

### Why this design minimizes cloud expenditures:
1. **Zero NAT Gateways**: Standard enterprise EKS blueprints deploy 2-3 NAT Gateways across Availability Zones ($32.40/month each + $0.045/GB data processing). Our FinOps blueprint uses public subnets with **tightly restricted Security Groups** and an Internet Gateway, **saving $64.80 - $97.20/month**.
2. **Single Scalable Worker Node**: Utilizes a single `t3.medium` burstable instance (2 vCPU, 4 GiB RAM) managed by an EKS Auto Scaling Group (min: 1, max: 2, desired: 1).
3. **Optimized Pod Footprint**:
   - `edusaas-lms`: Requests 50m CPU / 64Mi RAM (limits: 250m CPU / 256Mi RAM).
   - `finops-engine`: Requests 100m CPU / 128Mi RAM (limits: 500m CPU / 512Mi RAM).
   - Both workloads co-exist easily within the single `t3.medium` node (~3.8 GiB allocatable).

### Detailed Cost Estimation

| Component | AWS Resource | Specification | Hourly Rate (USD) | 3-Hour Evaluation (USD) | 1-Month (730 hrs) (USD) | 1-Month (INR approx @ ₹84/$)|
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Control Plane** | Amazon EKS Cluster | Managed EKS v1.31 | $0.1000 | $0.300 | $73.00 | ~₹6,132 |
| **Worker Compute** | EC2 Node Group | 1x `t3.medium` On-Demand | $0.0416 | $0.125 | $30.37 | ~₹2,551 |
| **Root Storage** | Amazon EBS | 20 GiB gp3 Storage | $0.0022 | $0.007 | $1.60 | ~₹134 |
| **Ingress Load Balancer** | Application Load Balancer | AWS ALB (Public) | $0.0225 | $0.068 | $16.43 | ~₹1,380 |
| **Public IPv4 Address** | AWS IPv4 Charge | 1x In-use Public IPv4 | $0.0050 | $0.015 | $3.65 | ~₹307 |
| **Container Registry** | Amazon ECR | 1x Image (~150 MB) | $0.0001 | $0.000 | $0.02 | ~₹2 |
| **Data Transfer** | Outbound Internet | < 1 GB test traffic | $0.0000 | $0.000 | $0.09 | ~₹8 |
| **TOTALS** | | | **~$0.1714 / hr** | **~$0.51 USD** | **~$125.16 USD** | **~₹10,514 INR** |

> **Cost Safeguard Recommendation:**
> - Run the automated deployment and verification test suite for **under 3 hours**, then immediately execute `teardown-aws.ps1`. Total billable expense will be **less than $1.00 USD (~₹84 INR)**.

---

## 3. Directory Structure

```
src/aws/
|-- cloudformation/
|   `-- eks-infrastructure.yaml       # Zero-NAT VPC, subnets, IGW, EKS cluster, node group, ECR repo
|-- k8s/
|   |-- namespace.yaml                # edusaas and finops-system namespaces
|   |-- edusaas-workload.yaml         # SaaS demo deployment, service, probes
|   |-- finops-platform.yaml          # FinOps FastAPI backend, dashboard, ClusterRole, ServiceAccount
|   |-- ingress-alb.yaml              # AWS ALB Ingress configuration
|   `-- hpa.yaml                      # HorizontalPodAutoscaler for SaaS workload
|-- scripts/
|   |-- deploy-aws.ps1                # Automated 1-click deployment & preflight validation
|   `-- teardown-aws.ps1              # Automated 1-click teardown & cost elimination
|-- Dockerfile                        # Multi-stage production container image
`-- README.md                         # This runbook
```

---

## 4. Prerequisites

1. **AWS Account**: Active AWS account with permissions to provision VPC, EKS, EC2, IAM, and ECR.
2. **AWS CLI v2**: Installed and configured (`aws configure` or IAM Identity Center SSO).
3. **Docker**: Installed and running (for building and pushing container images).
4. **kubectl**: Kubernetes CLI tool configured to interact with clusters.

---

## 5. Deployment Instructions

### Automated 1-Click Deployment (PowerShell)

```powershell
# Set AWS Region (default: us-east-1)
.\src\aws\scripts\deploy-aws.ps1 -Region "us-east-1"
```

### Manual Step-by-Step Deployment

#### Step 1: Pre-flight Identity Check
```bash
aws sts get-caller-identity
```

#### Step 2: Deploy CloudFormation Stack
```bash
aws cloudformation deploy \
  --template-file src/aws/cloudformation/eks-infrastructure.yaml \
  --stack-name KubeCostFinOps-EKS-Stack \
  --parameter-overrides ClusterName=kubecost-finops-eks NodeInstanceType=t3.medium \
  --capabilities CAPABILITY_NAMED_IAM \
  --region us-east-1
```

#### Step 3: Configure kubectl
```bash
aws eks update-kubeconfig --name kubecost-finops-eks --region us-east-1
kubectl get nodes
```

#### Step 4: Build and Push Docker Container to ECR
```bash
# Retrieve ECR URI
ECR_URI=$(aws cloudformation describe-stacks --stack-name KubeCostFinOps-EKS-Stack --region us-east-1 --query "Stacks[0].Outputs[?OutputKey=='ECRRepositoryUri'].OutputValue" --output text)

# Login to ECR
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin $ECR_URI

# Build and Push
docker build -t $ECR_URI:v1.0.0 -f src/aws/Dockerfile .
docker push $ECR_URI:v1.0.0
```

#### Step 5: Deploy Kubernetes Workloads
```bash
# Apply namespaces and workloads
kubectl apply -f src/aws/k8s/namespace.yaml
kubectl apply -f src/aws/k8s/edusaas-workload.yaml

# Deploy FinOps platform with real ECR URI
sed "s|123456789012.dkr.ecr.us-east-1.amazonaws.com/kubecost-finops-platform:v1.0.0|$ECR_URI:v1.0.0|g" src/aws/k8s/finops-platform.yaml | kubectl apply -f -

# Apply HPA and Ingress
kubectl apply -f src/aws/k8s/hpa.yaml
kubectl apply -f src/aws/k8s/ingress-alb.yaml
```

---

## 6. Post-Deployment Verification & Testing

### 1. Verify Workload Pods
```bash
kubectl get pods -n edusaas
kubectl get pods -n finops-system
```
Expected output: All pods status `Running` and `Ready 1/1`.

### 2. Verify API Health Check
```bash
# Port-forward if ALB is not publicly routed
kubectl port-forward svc/finops-service 8000:8000 -n finops-system &

# Test health check
curl http://localhost:8000/health
# Response: {"status":"healthy","version":"1.0.0","framework":"FinOps Intelligence Engine"}

# Test recommendations endpoint
curl http://localhost:8000/api/v1/recommendations
```

### 3. Verify Dashboard UI
Access `http://localhost:8000/` in your web browser to view the interactive live telemetry and rightsizing dashboard.

---

## 7. Teardown & Cost Elimination Runbook

To ensure no ongoing charges occur on your AWS bill, run the teardown script immediately after evaluation:

```powershell
.\src\aws\scripts\teardown-aws.ps1 -Region "us-east-1"
```

Manual teardown steps:
```bash
# 1. Delete Ingress to release AWS ALB
kubectl delete ingress finops-ingress -n finops-system
kubectl delete namespace finops-system edusaas

# 2. Delete ECR Images
aws ecr batch-delete-image --repository-name kubecost-finops-platform --image-ids imageTag=v1.0.0 --region us-east-1

# 3. Delete CloudFormation Stack
aws cloudformation delete-stack --stack-name KubeCostFinOps-EKS-Stack --region us-east-1
aws cloudformation wait stack-delete-complete --stack-name KubeCostFinOps-EKS-Stack --region us-east-1
```
