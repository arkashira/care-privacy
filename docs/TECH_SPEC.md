# TECH_SPEC.md  

**Project:** `care-privacy`  
**Domain:** Consent Management & Data Protection for AI‑enabled systems in Healthcare & Education  
**Owner:** Axentx – Product/Engineering Lead  
**Status:** Draft (ready for review & implementation)  

---  

## 1. Overview  

`care-privacy` is a SaaS platform that enables organizations in the healthcare and education sectors to **collect, store, manage, and audit user consent** for the processing of personal and sensitive data by AI/ML services.  

Key goals:  

| Goal | Description |
|------|-------------|
| **Regulatory compliance** | Supports HIPAA, GDPR, FERPA, and emerging AI‑specific regulations (e.g., EU AI Act). |
| **Fine‑grained consent** | Consent can be scoped per data type, purpose, AI model, and retention period. |
| **Auditability** | Immutable consent logs with cryptographic proof of integrity. |
| **Interoperability** | Open APIs (REST & GraphQL) and SDKs for integration with existing EHR/LMS, data pipelines, and model serving stacks (vLLM, SGLang). |
| **Scalable & secure** | Cloud‑native, zero‑trust architecture, data‑at‑rest encryption, and role‑based access control (RBAC). |

---  

## 2. Architecture Overview  

```
+-------------------+        +-------------------+        +-------------------+
|  Client Apps      | <---> |  API Gateway      | <---> |  Auth Service     |
| (Web, Mobile,    |        | (Kong/Envoy)      |        | (OAuth2/OIDC)     |
|  SDKs)            |        +-------------------+        +-------------------+
+-------------------+                |                         |
                                      |                         |
                                      v                         v
+-------------------+        +-------------------+        +-------------------+
| Consent Service   | <----> | Data Store (SQL)  | <----> | Audit Service     |
| (Core Business)  |        | + Postgres +      |        | (Append‑only log) |
|                   |        |   TimescaleDB)    |        +-------------------+
+-------------------+        +-------------------+                |
        |                         ^                               |
        |                         |                               |
        v                         |                               v
+-------------------+   Event Bus (Kafka)   +-------------------+   +-------------------+
| Policy Engine     | <------------------- | Notification svc |   | Reporting / BI   |
| (OPA + Rules)     |                     | (Email, Webhook) |   | (Superset)       |
+-------------------+                     +-------------------+   +-------------------+
```

### Core Components  

| Component | Responsibility | Tech |
|-----------|----------------|------|
| **API Gateway** | TLS termination, request routing, rate limiting, API key management | Kong (Docker) |
| **Auth Service** | OAuth2/OIDC, SSO, MFA, token issuance | Keycloak (v24) |
| **Consent Service** | CRUD of consent records, versioning, revocation workflow | FastAPI (Python 3.11) |
| **Policy Engine** | Evaluate consent against request context (data type, purpose, model) | Open Policy Agent (OPA) + Rego policies |
| **Data Store** | Persistent, relational storage of consent metadata & user profiles | PostgreSQL 15 + TimescaleDB extension for time‑series audit logs |
| **Audit Service** | Immutable append‑only log, cryptographic hash chaining, export to WORM storage | Kafka + Confluent Schema Registry + S3 (object lock) |
| **Notification Service** | Send consent request, revocation, and expiry alerts | Celery + Redis broker + SMTP / Twilio |
| **Reporting / BI** | Dashboards for compliance officers, export CSV/JSON | Apache Superset |
| **SDKs** | Client libraries for Java, Python, JavaScript/TypeScript | Published to internal PyPI & npm registry |

---  

## 3. Data Model  

### 3.1 Core Tables (PostgreSQL)

| Table | Primary Key | Important Columns | Description |
|-------|-------------|-------------------|-------------|
| `users` | `user_id` (UUID) | `email`, `full_name`, `sector` (enum: healthcare, education), `created_at` | Identity of the data subject. |
| `consents` | `consent_id` (UUID) | `user_id`, `data_category`, `purpose`, `model_id`, `valid_from`, `valid_until`, `status` (enum: active, revoked, expired), `version`, `signature_hash` | One consent record per scope. |
| `models` | `model_id` (UUID) | `name`, `owner_org`, `description`, `sensitivity_level` (enum), `created_at` | AI/ML models that may process data. |
| `audit_logs` | `log_id` (BIGINT) | `consent_id`, `action` (enum), `performed_by`, `timestamp`, `hash_chain` | Immutable log; stored in TimescaleDB hypertable. |
| `policy_rules` | `rule_id` (UUID) | `resource`, `effect` (allow/deny), `condition` (Rego JSON), `created_at` | Dynamically loaded into OPA. |

### 3.2 JSONB Fields  

- `consents.metadata` (JSONB): optional free‑form key/value for custom attributes (e.g., device ID).  
- `audit_logs.payload` (JSONB): snapshot of request context for forensic analysis.  

### 3.3 Cryptographic Guarantees  

- Each consent version is signed with the platform’s ECDSA‑P256 private key; `signature_hash` stores the base64 signature.  
- Audit log entries include a **hash chain**: `hash_i = H(hash_{i-1} || log_i)`. The latest hash is published daily to an external immutable ledger (e.g., AWS QLDB) for third‑party verification.  

---  

## 4. Key APIs / Interfaces  

All endpoints are versioned under `/api/v1`. OpenAPI 3.1 spec is generated automatically (`/docs/openapi.json`).  

### 4.1 REST Endpoints  

| Method | Path | Auth | Description |
|--------|------|------|-------------|
| `POST` | `/consents` | Bearer (client‑app) | Create a new consent record. Body: `ConsentCreateDTO`. |
| `GET` | `/consents/{id}` | Bearer | Retrieve consent (latest version). |
| `PATCH` | `/consents/{id}` | Bearer | Update consent (e.g., extend expiry). |
| `DELETE` | `/consents/{id}` | Bearer | Revoke consent (status → revoked). |
| `GET` | `/users/{id}/consents` | Bearer | List all consents for a user. |
| `POST` | `/audit/query` | Bearer (admin) | Query audit logs with time‑range filters. |
| `GET` | `/policies` | Bearer (admin) | List active OPA policies. |
| `POST` | `/policies` | Bearer (admin) | Upload/replace a policy rule. |

### 4.2 GraphQL  

- Endpoint: `/graphql` (protected by same OAuth2 token).  
- Schema exposes `user`, `consent`, `model`, and `auditLog` types with filter arguments. Useful for UI dashboards and ad‑hoc compliance queries.  

### 4.3 SDK Interfaces  

| Language | Package | Core Functions |
|----------|---------|----------------|
| Python | `care_privacy_sdk` | `request_consent(user_id, scope)`, `check_consent(user_id, model_id, data_category)`, `revoke_consent(consent_id)` |
| JavaScript/TypeScript | `@care-privacy/sdk` | Same as Python, plus React hook `useConsentStatus`. |
| Java | `com.careprivacy.sdk` | Same as Python, with Spring Boot starter. |

All SDKs internally call the REST API and perform token refresh via Keycloak.  

---  

## 5. Technology Stack  

| Layer | Technology | Version | Rationale |
|-------|------------|---------|-----------|
| **API** | FastAPI | 0.110 | High performance, async, automatic OpenAPI generation. |
| **Auth** | Keycloak | 24.0 | Enterprise‑grade OIDC, SSO, MFA, LDAP integration. |
| **Gateway** | Kong | 3.5 (Docker) | Mature plugin ecosystem (rate‑limit, request‑transform). |
| **Policy** | OPA | 0.58 | Decoupled, declarative policy evaluation. |
| **DB** | PostgreSQL | 15 | Strong ACID guarantees, TimescaleDB for audit time‑series. |
| **Message Bus** | Apache Kafka | 3.6 | Guarantees ordered immutable audit stream. |
| **Task Queue** | Celery + Redis | Celery 5.4, Redis 7 | Reliable background processing (email, webhook). |
| **Container Runtime** | Docker Compose (dev) / Kubernetes (prod) | - | Portable dev environment, auto‑scaling in prod. |
| **CI/CD** | GitHub Actions + ArgoCD | - | Automated tests, canary deployments. |
| **Observability** | Prometheus + Grafana | - | Metrics for latency, error rates, consent throughput. |
| **Logging** | Loki + Fluent Bit | - | Centralised log aggregation. |
| **Secrets Management** | HashiCorp Vault | 1.15 | Stores DB credentials, signing keys, OIDC client secrets. |
| **Infrastructure as Code** | Terraform (AWS) | - | Reproducible cloud provisioning (RDS, EKS, S3). |

---  

## 6. Dependencies  

| Dependency | License | Usage |
|------------|---------|-------|
| `vLLM` | Apache‑2.0 | Example AI model serving integration (demo). |
| `SGLang` | Apache‑2.0 | Structured generation example for consent text. |
| `psycopg2-binary` | LGPL‑3.0 | PostgreSQL driver for FastAPI. |
| `python-jose` | MIT | JWT handling for token verification. |
| `opa` | Apache‑2.0 | Policy evaluation engine. |
| `kafka-python` | Apache‑2.0 | Producer for audit events. |
| `celery[redis]` | BSD-3 | Background job processing. |
| `pydantic` | MIT | Data validation for request/response models. |

All dependencies are pinned in `requirements.txt` and `package.json`.  

---  

## 7. Deployment Architecture  

### 7.1 Production (AWS)  

| Component | Service | Instance Type | Autoscaling |
|-----------|---------|---------------|-------------|
| API + Consent Service | EKS (Fargate) | `cpu: 0.5 vCPU, mem: 1Gi` | Horizontal pod autoscaler (target RPS 2000) |
| Auth (Keycloak) | RDS PostgreSQL + EC2 (t3.medium) | 2 nodes (HA) | N/A |
| OPA | Sidecar in each API pod | Shared memory | N/A |
| Kafka | MSK (3‑node) | `kafka.m5.large` | N/A |
| PostgreSQL | RDS Aurora Serverless v2 | Auto‑scale | N/A |
| Redis (Celery broker) | ElastiCache (cluster) | `cache.r5.large` | N/A |
| Object Store (audit immutable) | S3 with Object Lock | Standard | N/A |
| Monitoring | CloudWatch + Prometheus (EKS) | — | — |
| CI/CD | GitHub Actions → ArgoCD (EKS) | — | — |

All traffic is forced through **AWS PrivateLink** and **WAF**. TLS termination at Kong (managed certs via ACM).  

### 7.2 Staging  

- Same topology as prod but with reduced instance sizes and a separate VPC.  
- Database snapshots refreshed nightly from prod (PII masked).  

### 7.3 Development  

- Docker Compose with local PostgreSQL, Redis, and a single‑node Kafka.  
- Hot‑reload enabled for FastAPI (`uvicorn --reload`).  

---  

## 8. Security & Compliance  

| Area | Controls |
|------|----------|
| **Data at Rest** | AES‑256 encryption (RDS, S3). |
| **Data in Transit** | TLS 1.3 everywhere; mTLS between services (OPA sidecar). |
| **Access Control** | RBAC via Keycloak groups (`admin`, `compliance`, `client-app`). |
| **Auditability** | Append‑only Kafka log + daily hash anchor to immutable ledger. |
| **PII Masking** | Automated masking of `email` in non‑prod DB dumps. |
| **Vulnerability Scanning** | Trivy CI step; weekly dependency updates. |
| **Pen‑Test** | External audit every 6 months; internal OWASP ZAP scans per PR. |
| **Backup & DR** | RDS automated backups (7‑day retention), cross‑region S3 replication. |

---  

## 9. Testing Strategy  

| Test Type | Tools | Coverage Goal |
|-----------|-------|---------------|
| Unit | pytest, hypothesis | 90 % per module |
| Integration | Testcontainers (Postgres, Kafka) | 80 % of API flows |
| Contract | Schemathesis (OpenAPI) | 100 % of public endpoints |
| Performance | locust.io (consent create 5k RPS) | ≤ 150 ms 95th percentile |
| Security | bandit, OWASP ZAP | No critical findings |
| End‑to‑End | Cypress (React admin UI) | Core user journeys (request, revoke, audit) |

All tests run in CI; gate requires **≥ 85 % overall coverage**.  

---  

## 10. Roadmap (Post‑MVP)  

| Milestone | Features | Target |
|-----------|----------|--------|
| **MVP** | Core consent CRUD, OPA policies, audit log, SDKs, admin UI | Q3 2026 |
| **Version 1.1** | Consent templates, multi‑language UI, bulk import/export | Q4 2026 |
| **Version 1.2** | Federated consent across multiple institutions (SCIM sync) | Q1 2027 |
| **Version 2.0** | AI‑model‑aware consent (dynamic purpose inference), blockchain anchoring | Q3 2027 |

---  

## 11. Glossary  

- **Consent Record** – A signed, versioned statement from a data subject granting permission for a specific data processing purpose.  
- **OPA** – Open Policy Agent, used for evaluating consent at request time.  
- **Hash Chain** – Cryptographic linking of audit entries to guarantee immutability.  
- **Sector** – Either `healthcare` or `education`; influences default policy sets.  

---  

*Prepared by:* Senior Product/Engineering Lead, Axentx  
*Date:* 2026‑06‑19  

---
