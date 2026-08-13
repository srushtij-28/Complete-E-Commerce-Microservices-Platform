# Complete E-Commerce Microservices Platform

A production-style e-commerce backend demonstrating modern distributed-system architecture.

## Architecture

```text
Client
  │
  ▼
API Gateway
  │
  ├── User Service
  ├── Product Service
  ├── Cart Service
  └── Order Service
           │
           ▼
     Saga Orchestrator
       │     │     │
       ▼     ▼     ▼
  Inventory Payment Shipping
       │     │     │
       └─────┼─────┘
             ▼
           Kafka
             │
       ┌─────┴─────┐
       ▼           ▼
    Audit     Notification
```

## Technologies

- Python
- Flask
- MySQL
- SQLAlchemy
- Redis
- Kafka
- Elasticsearch
- Docker
- Kubernetes
- NGINX
- Prometheus
- Grafana
- OpenTelemetry
- Jaeger
- HashiCorp Vault

## Core Features

- User authentication
- Product management
- Product search
- Shopping cart
- Order management
- Inventory reservation
- Payment workflow
- Webhook processing
- Idempotency
- Saga orchestration
- Kafka events
- Audit logging
- Notifications
- Distributed caching
- Rate limiting
- Observability
- Health checks

## Run

```bash
docker compose up --build
```

## Purpose

Day 300 combines the major backend, distributed-system, security, messaging, observability, and deployment concepts developed throughout the 300-day project series.
