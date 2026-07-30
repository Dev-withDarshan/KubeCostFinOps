# 🔐 IAM Policies

This folder will contain **AWS IAM policy documents** that define least-privilege access for each service and role in the framework.

## Planned Policies

| Policy File | Target | Purpose |
|------------|--------|---------|
| `lambda_execution_role.json` | Lambda functions | Permissions for S3, DynamoDB, SageMaker, and EKS access |
| `sagemaker_execution_role.json` | SageMaker | Permissions for S3 data access and model artifact storage |
| `api_gateway_policy.json` | API Gateway | Permissions to invoke Lambda and access Cognito |
| `eks_node_role.json` | EKS worker nodes | Permissions for ECR pull, CloudWatch logging, and S3 access |

## Owner

**Dhanushkodi** — Backend Developer & DevOps Engineer (`feature/dhanushkodi` branch)

> **Note:** Implementation will begin in Phase-II. See also `security/iam_least_privilege_policy.json` for the baseline security policy.
