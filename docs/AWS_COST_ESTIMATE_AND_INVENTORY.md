# AWS Production Cost Estimate & Resource Inventory

**Project Title:** Kubernetes Cost Optimization Framework for SaaS-Based Educational Platforms using FinOps Intelligence  
**Target Platform:** Amazon Elastic Kubernetes Service (Amazon EKS)  
**Target AWS Region:** `us-east-1` (US East, N. Virginia)  
**Reference Date:** Academic Year 2025–2026  

---

## 1. Architectural Cost Design Principles

To adhere strictly to FinOps principles and eliminate unnecessary educational/research cloud overhead, the infrastructure is engineered as an **Ultra-Low-Cost, Zero-NAT-Gateway architecture**:
1. **No NAT Gateways**: Bypasses AWS NAT Gateway charges ($32.40/month per gateway + data processing charges) by using public subnets with strictly locked-down AWS Security Groups.
2. **Minimal Worker Footprint**: Uses a single burstable `t3.medium` instance (2 vCPUs, 4 GiB RAM) managed by an EKS Node Group (desired: 1, min: 1, max: 2).
3. **Application Load Balancer (ALB)**: Provides a single ingress entry point for both the FinOps dashboard and REST API routes.
4. **Advisory Non-Mutating Execution**: Recommendations are calculated and previewed without mutating live cluster state unless explicitly authorized.

---

## 2. Resource Inventory & Pricing Breakdown

| # | Resource Type | AWS Resource Name / Identifier | Spec / Configuration | Purpose | Hourly Cost (USD) | 3-Hour Evaluation (USD) | Monthly Cost (730 hrs, USD) | Approx Monthly (INR @ ₹84/$) |
|---|---|---|---|---|---|---|---|---|
| 1 | **EKS Control Plane** | `kubecost-finops-eks` | Kubernetes v1.31 Managed Control Plane | Core orchestration & API server | $0.1000 | $0.300 | $73.00 | ~₹6,132 |
| 2 | **EC2 Worker Node** | `eks-nodegroup-t3-medium` | 1x `t3.medium` (2 vCPU, 4 GiB) | Runs EduSaaS & FinOps Pods | $0.0416 | $0.125 | $30.37 | ~₹2,551 |
| 3 | **EBS Root Volume** | Attached gp3 Volume | 20 GiB gp3 Storage (3,000 IOPS) | OS & Container filesystem | $0.0022 | $0.007 | $1.60 | ~₹134 |
| 4 | **Ingress Controller** | `finops-ingress` (AWS ALB) | 1x Application Load Balancer | External HTTPS/HTTP routing | $0.0225 | $0.068 | $16.43 | ~₹1,380 |
| 5 | **Public IPv4 Charge** | Attached to EC2/ALB | 1x In-use Public IPv4 address | AWS standard public IPv4 fee | $0.0050 | $0.015 | $3.65 | ~₹307 |
| 6 | **Container Registry** | `kubecost-finops-platform` | Amazon ECR (< 200 MB storage) | Stores container images | $0.0001 | $0.000 | $0.02 | ~₹2 |
| 7 | **CloudWatch & Logs** | Basic / Metric Server | Default log retention (no active vended logs) | Basic pod health monitoring | $0.0000 | $0.000 | $0.00 | ~₹0 |
| 8 | **Data Transfer** | Internet Egress | < 1 GB evaluated data transfer | Frontend and API traffic | $0.0000 | $0.000 | $0.09 | ~₹8 |
| **TOTAL** | | | | | **~$0.1714 / hr** | **~$0.51 USD** | **~$125.16 USD** | **~₹10,514 INR** |

*Note: USD to INR conversion is approximate based on a reference exchange rate of ₹84.00 per USD.*

---

## 3. Assumptions and Exclusions

1. **Spot vs. On-Demand**: The calculation above assumes standard On-Demand pricing. If Spot Instances are utilized for the `t3.medium` node group, compute costs decrease by ~65% ($10.63/month vs $30.37/month).
2. **Free Tier Applicability**: AWS Free Tier offers 750 hours/month of `t2.micro` or `t3.micro` for the first 12 months, but EKS control plane ($0.10/hr) has **no free tier** discount. Therefore, EKS control plane is always billable.
3. **Data Egress**: Standard evaluation runs generate minimal data transfer (< 100 MB), remaining well within the AWS 100 GB/month free internet egress allowance.
4. **NAT Gateway Exclusion**: If an enterprise auditor requests private subnets with NAT Gateways in 2 AZs, this will add **$64.80/month (~₹5,443 INR)** plus data processing fees.

---

## 4. Teardown Procedure & Zero Ongoing Charge Guarantee

Executing `src/aws/scripts/teardown-aws.ps1` performs the following automated cleanup:
1. Deletes Kubernetes Ingress (`finops-ingress`) in namespace `finops-system`, immediately releasing the AWS Application Load Balancer.
2. Deletes namespaces `finops-system` and `edusaas`.
3. Purges all container images from ECR repository `kubecost-finops-platform`.
4. Deletes CloudFormation stack `KubeCostFinOps-EKS-Stack`, destroying the EKS cluster, Node Group, VPC, Subnets, and Security Groups.
5. Verifies via `aws eks describe-cluster` that no running resources remain.
6. **Resulting ongoing hourly billable expense: $0.00 / hour.**
