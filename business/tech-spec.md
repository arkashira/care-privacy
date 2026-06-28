Here is the full `tech-spec.md` — paste it directly into the repo:

---

# care-privacy — Technical Specification v1

> Consent management and data protection platform for AI/tech products in healthcare and education.
> Compliance targets: HIPAA, FERPA, GDPR, CCPA.

---

## Stack

| Layer | Choice | Rationale |
|---|---|---|
| **Language** | Python 3.12 | HIPAA/security ecosystem depth; FastAPI async perf |
| **API framework** | FastAPI 0.111 | Pydantic v2 validation, OpenAPI auto-docs, async-native |
| **Task queue** | Celery 5 + Redis 7 | Audit log fan-out, consent expiry jobs, webhook delivery |
| **ORM** | SQLAlchemy 2 (async) | Typed models, Alembic migrations |
| **DB** | PostgreSQL 16 | Row-level security, JSONB for flexible consent metadata |
| **Cache / broker** | Redis 7 (Upstash free tier) | Session tokens, rate-limit counters, Celery broker |
| **Auth** | python-jose (JWT RS256) + passlib | Asymmetric keys; rotate without secret sharing |
| **Frontend** | Next.js 14 (App Router) + shadcn/ui | Consent banner SDK, admin dashboard |
| **SDK (embeddable)** | Vanilla JS < 8 KB (ESM) | Drop-in consent banner for third-party AI products |
| **Runtime** | Python 3.12 on Docker (linux/amd64) | Reproducible; Render/Railway compatible |

---

## Hosting (free-tier-first)

| Component | Platform | Free Tier Limit | Upgrade Trigger |
|---|---|---|---|
| API server | Render (Web Service) | 750 hr/mo, 512 MB RAM | > 1k req/min |
| PostgreSQL | Neon (serverless) | 0.5 GB storage, 1 branch | > 500 MB or prod branch |
| Redis / broker | Upstash Redis | 10k cmd/day | Celery > 10k tasks/day |
| Frontend / dashboard | Vercel Hobby | 100 GB bandwidth | Custom domain + team |
| Object storage (audit exports) | Cloudflare R2 | 10 GB + 1M ops/mo | Export volume |
| Secrets | Doppler (free) | Unlimited envs | Team SSO |
| CI/CD | GitHub Actions (free) | 2k min/mo | Matrix test expansion |

**Production path:** Render Starter ($7/mo) + Neon Pro ($19/mo) handles ~50k monthly active data-subjects.

---

## Data Model

### `tenants`
```
id            uuid PK
name          text NOT NULL
plan          text DEFAULT 'free'          -- free | starter | hipaa
hipaa_baa     boolean DEFAULT false
created_at    timestamptz
```

### `data_subjects`
```
id            uuid PK
tenant_id     uuid FK tenants
external_id   text NOT NULL               -- caller's own user/patient/student ID
email_hash    text                        -- SHA-256, lookup without storing PII
jurisdiction  text                        -- 'US-HIPAA' | 'US-FERPA' | 'EU-GDPR' | 'US-CCPA'
created_at    timestamptz
UNIQUE (tenant_id, external_id)
```

### `purposes`
```
id            uuid PK
tenant_id     uuid FK tenants
slug          text NOT NULL               -- 'ai-training' | 'analytics' | 'third-party-sharing'
label         text NOT NULL
legal_basis   text                        -- 'consent' | 'legitimate-interest' | 'contract'
retention_days int                        -- NULL = indefinite
UNIQUE (tenant_id, slug)
```

### `consents`
```
id            uuid PK
tenant_id     uuid FK tenants
subject_id    uuid FK data_subjects
purpose_id    uuid FK purposes
status        text                        -- 'granted' | 'withdrawn' | 'pending' | 'expired'
granted_at    timestamptz
expires_at    timestamptz                 -- NULL = no expiry
withdrawn_at  timestamptz
ip_address    inet
user_agent    text
proof_hash    text                        -- SHA-256(subject_id||purpose_id||granted_at||nonce)
```

### `audit_events`
```
id            uuid PK
tenant_id     uuid FK tenants
actor_id      text                        -- API key id or user id
event_type    text NOT NULL               -- 'consent.granted' | 'consent.withdrawn' | 'data.accessed'
subject_id    uuid FK data_subjects NULL
payload       jsonb                       -- full event snapshot
occurred_at   timestamptz NOT NULL
```
> Append-only. Application role has INSERT only on this table; no UPDATE/DELETE.

### `api_keys`
```
id            uuid PK
tenant_id     uuid FK tenants
key_hash      text UNIQUE NOT NULL        -- bcrypt; raw key shown once at creation
scopes        text[]                      -- ['consent:read','consent:write','audit:read']
expires_at    timestamptz
revoked_at    timestamptz
```

---

## API Surface

All endpoints: `Content-Type: application/json`, versioned under `/v1`.
Auth: `Authorization: Bearer <api_key>` (server-to-server) or RS256 JWT cookie (dashboard).

| # | Method | Path | Purpose |
|---|---|---|---|
| 1 | `POST` | `/v1/consents` | Record a consent grant or withdrawal for a subject + purpose |
| 2 | `GET` | `/v1/consents` | Query consent status (`?external_id=&purpose=`) — AI pipeline gate |
| 3 | `GET` | `/v1/consents/{id}` | Fetch single record with proof hash for audit |
| 4 | `DELETE` | `/v1/consents/{id}` | Withdraw consent (soft-delete, sets `withdrawn_at`) |
| 5 | `GET` | `/v1/subjects/{external_id}/export` | DSAR: full data export (GDPR Art. 15 / HIPAA §164.524) |
| 6 | `DELETE` | `/v1/subjects/{external_id}` | Right-to-erasure: anonymize all subject records |
| 7 | `GET` | `/v1/purposes` | List all consent purposes for this tenant |
| 8 | `POST` | `/v1/purposes` | Create a purpose with legal basis + retention policy |
| 9 | `GET` | `/v1/audit` | Query audit log (`?from=&to=&event_type=&subject_id=`) paginated |
| 10 | `POST` | `/v1/webhooks` | Register URL for real-time consent-change events |

**SDK shortcut** (embeddable consent banner):
```
GET /v1/banner/{tenant_slug}?subject={ext_id}
```
Returns JSON config consumed by the < 8 KB vanilla JS bundle.

---

## Security Model

### Authentication
- **API keys**: HMAC-SHA256 keyed lookup; bcrypt-hashed at rest; raw key shown once. Scoped per operation group.
- **Dashboard users**: RS256 JWT, 15-min access token + 7-day refresh (httpOnly cookie, SameSite=Strict).
- **Tenant isolation**: Every query includes `WHERE tenant_id = :tenant_id` at ORM layer AND enforced via PostgreSQL Row-Level Security as defense-in-depth.

### Secrets
- All secrets (DB URL, Redis URL, JWT private key) injected via environment from Doppler.
- 2048-bit RSA key pair for JWT signing; private key never leaves API container; public key at `/.well-known/jwks.json`.
- API key rotation: 24h overlap window; old key marked `revoked_at` after grace period.

### Data Protection
- Email stored as SHA-256 hash only; IP addresses encrypted at column level via pgcrypto AES-256-GCM.
- TLS 1.3 enforced at load balancer; HSTS preload.
- HIPAA BAA tenants: isolated to dedicated Neon branch + separate Redis namespace.

### IAM (least privilege)

| DB Role | Permissions |
|---|---|
| `api_app` | SELECT/INSERT/UPDATE on consents, subjects, purposes; INSERT on audit_events |
| `audit_writer` | INSERT only on audit_events |
| `migration_runner` | DDL (CI only, short-lived) |
| `readonly_analyst` | SELECT on audit_events, purposes (no PII tables) |

---

## Observability

### Logs
- Structured JSON via `structlog`; fields: `tenant_id`, `request_id`, `event`, `duration_ms`, `status_code`.
- Sink: stdout → Render log drain → **Papertrail free** (48h retention); upgrade to Datadog on first enterprise deal.

### Metrics
- `prometheus_fastapi_instrumentator` at `/metrics`.
- Key metrics: `consent_grants_total{tenant,purpose}`, `consent_withdrawals_total`, `api_latency_seconds{endpoint}`, `active_subjects_gauge`.
- Scraped by **Grafana Cloud free** (10k series limit).

### Traces
- `opentelemetry-sdk` + OTLP exporter; SQLAlchemy + Celery auto-instrumented.
- Backend: **Grafana Tempo** via Grafana Cloud free (14-day retention).
- Sampling: 100% dev, 10% prod (head-based), 100% on errors.

### Alerts
- P0: API error rate > 1% over 5 min → PagerDuty free tier.
- P1: Consent expiry job lag > 1h → Slack webhook.
- P2: Audit log write failures → Slack webhook.

---

## Build / CI

### Repository layout
```
care-privacy/
├── api/                  # FastAPI app
│   ├── routers/
│   ├── models/           # SQLAlchemy
│   ├── schemas/          # Pydantic
│   └── services/
├── worker/               # Celery tasks (expiry, webhooks, DSAR jobs)
├── sdk/                  # Vanilla JS consent banner (< 8 KB ESM)
├── dashboard/            # Next.js 14
├── migrations/           # Alembic
├── tests/
│   ├── unit/
│   └── integration/      # testcontainers: real Postgres + Redis
├── Dockerfile
├── docker-compose.yml    # local dev
└── .github/workflows/
```

### GitHub Actions pipeline
```yaml
on: [push, pull_request]

jobs:
  lint:
    - ruff check + ruff format --check
    - eslint + prettier

  test:
    - pytest --cov=api --cov-fail-under=80
    - testcontainers: Postgres 16 + Redis 7
    - HIPAA scenario: grant → AI gate check → withdraw → re-check

  security:
    - trivy fs . (CVE scan)
    - bandit -r api/ (Python SAST)
    - semgrep --config=p/owasp-top-ten

  build:
    - docker build --platform linux/amd64 -t care-privacy:$SHA .
    - push to ghcr.io

  deploy (main only):
    - alembic upgrade head (Render pre-deploy job)
    - render deploy hook
    - vercel --prod (dashboard)
```

### Quality gates
- Merge blocked if: lint fails, coverage < 80%, any CRITICAL Trivy CVE, or bandit HIGH finding.
- Dependabot: weekly Python + npm PRs, auto-merged if CI green.

---

*Generated: 2026-06-19 | care-privacy v1 | Axentx OS*

---

Key decisions worth noting:

- **Proof hash on every consent record** — cryptographic non-repudiation is required for HIPAA audit trails; SHA-256(subject||purpose||timestamp||nonce) lets you prove a grant happened without trusting only the DB.
- **Append-only audit table with a write-only DB role** — the application literally cannot mutate or delete audit records, which satisfies HIPAA §164.312(b) technical audit controls.
- **HIPAA BAA tenants get a separate Neon branch** — Neon's branching maps cleanly to tenant isolation without running a second cluster, keeping costs at zero until revenue justifies it.
- **< 8 KB vanilla JS SDK** — the drop-in consent banner must load inside EHR and LMS iframes that block frameworks; no React dependency.