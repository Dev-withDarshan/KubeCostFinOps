# KMS Key Policy Notes

## Purpose

This document outlines the intended AWS KMS key policy for encrypting sensitive data
within the Kubernetes Cost Optimization Framework.

## Planned Encryption Scope

| Data Category | AWS Service | Encryption Method |
|---------------|-------------|-------------------|
| Model artifacts | S3 | SSE-KMS |
| Database at rest | RDS (PostgreSQL) | KMS-managed key |
| Secrets | Kubernetes Secrets | EKS envelope encryption via KMS |
| DynamoDB tables | DynamoDB | AWS-managed or CMK |

## Key Policy — TODO

> **Placeholder:** The actual KMS key policy JSON and key rotation configuration
> will be defined during Phase-II when the AWS infrastructure is provisioned.

Key considerations:
- Restrict `kms:Decrypt` to the EKS node IAM role and SageMaker execution role only.
- Enable automatic key rotation (annual).
- Deny key deletion without MFA.
