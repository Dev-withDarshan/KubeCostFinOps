# ⚙️ Backend — Application API Server

This folder will contain the **Node.js** backend API server that bridges the frontend dashboard with the FinOps engine, ML model, and databases.

## Purpose

- RESTful API endpoints for cost data retrieval, recommendation management, and user authentication
- Integration with Amazon RDS (PostgreSQL) for persistent data and DynamoDB for real-time metrics
- Proxy layer between the React frontend and the Python FinOps engine
- Webhook endpoints for receiving Prometheus alerts

## Planned Technology

| Technology | Purpose |
|-----------|---------|
| Node.js + Express.js | API server framework |
| Sequelize / Knex.js | PostgreSQL ORM / query builder |
| AWS SDK for JavaScript | DynamoDB, S3, Cognito integration |
| Jest | Unit testing |

## Owner

**Dhanushkodi** — Backend Developer & DevOps Engineer (`feature/dhanushkodi` branch)

> **Note:** Implementation will begin in Phase-II. This folder currently serves as a placeholder.
