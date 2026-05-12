# AmaniPulse AI Backend

This is the first FastAPI backend implementation for the AmaniPulse AI iPhone Citizen MVP.

It gives the iPhone app concrete APIs for anonymous report submission, report status, incident taxonomy, county risk guidance, app configuration, and localized safety resources.

## Current Scope

Implemented now:

- FastAPI application under `app/`.
- Versioned `/v1` API routes.
- Anonymous report submission contract.
- Report status lookup.
- English and Swahili incident taxonomy.
- County risk guidance.
- App configuration.
- Localized safety resources.
- Deterministic MVP AI pipeline placeholder.
- In-memory repositories for local development.
- PostgreSQL/PostGIS SQLAlchemy models.
- Alembic migration for report and county risk tables.
- Baseline risk guidance seeded for all 47 Kenya counties.
- Hashed internal review API keys with reviewer identity derived from the token.
- Request ID middleware and safe structured request logs with no report text.
- Readiness checks for deployment health probes.
- Public report payload-size and rate-limit controls.
- Production Dockerfile and backend deployment runbook.
- Tests for the core API contracts.

Prepared for next:

- Redis/Celery async processing.
- Encrypted report storage.
- Human review queue.
- Production deployment.

## Run Locally

From this directory:

```bash
uv sync --dev
uv run uvicorn app.main:app --reload
```

Open:

```text
http://127.0.0.1:8000/docs
```

By default, the API uses in-memory storage so the app can run without local infrastructure.

## Run With PostgreSQL/PostGIS

Start local services:

```bash
docker compose up -d postgres redis
```

Run migrations:

```bash
STORAGE_BACKEND=postgres uv run alembic upgrade head
```

Start the API with PostgreSQL persistence:

```bash
STORAGE_BACKEND=postgres uv run uvicorn app.main:app --reload
```

Run the Celery worker in a second terminal when `CELERY_TASK_ALWAYS_EAGER=false`:

```bash
STORAGE_BACKEND=postgres CELERY_TASK_ALWAYS_EAGER=false uv run celery \
  -A app.workers.celery_app.celery_app worker --loglevel=info
```

The default database URL is:

```text
postgresql+asyncpg://amanipulse:amanipulse@localhost:55432/amanipulse
```

The compose file maps container Postgres `5432` to host `55432` to avoid colliding with
local Postgres installations.

Generate a real report encryption key before pilot or production use:

```bash
uv run python -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())"
```

Then set:

```bash
REPORT_ENCRYPTION_KEY=<generated-key>
```

## Test

```bash
uv run pytest
uv run ruff check .
```

Run Postgres-backed integration tests when Docker services are up:

```bash
RUN_POSTGRES_TESTS=1 STORAGE_BACKEND=postgres uv run pytest tests/integration
```

## Build Container

From the repository root:

```bash
docker build -t amanipulse-backend ./backend
docker run --rm -p 8000:8000 --env-file backend/.env amanipulse-backend
```

Run migrations once per release before routing traffic:

```bash
STORAGE_BACKEND=postgres uv run alembic upgrade head
```

See `docs/deployment.md` for the backend deployment runbook.

## API Endpoints

```text
GET  /v1/health
GET  /v1/ready
GET  /v1/incident-taxonomy?language=en
POST /v1/reports
GET  /v1/reports/{report_reference}/status
GET  /v1/risk/county/{county_code}
GET  /v1/app-config?platform=ios&version=1.0.0&language=en
GET  /v1/resources?language=sw&country=KE
GET  /v1/internal/review/queue
GET  /v1/internal/review/reports/{report_reference}
POST /v1/internal/review/reports/{report_reference}/decision
GET  /v1/internal/review/reports/{report_reference}/events
```

## Architecture

The iPhone app should remain a safe reporting client. It should not own peace intelligence or AI decisions.

Backend responsibilities:

- Receive anonymous reports.
- Validate and minimize data.
- Encrypt sensitive report descriptions before storing them.
- Run classification and escalation logic.
- Add non-sensitive PII/safety flags for human reviewers.
- Update aggregated county risk guidance.
- Keep high-risk reports available for future human review.
- Serve calm, public, non-sensitive guidance back to the iPhone app.

## Observability

Every response includes a request ID header. Clients may send `X-Request-ID`; otherwise the
API generates one. Request logs include only production-safe metadata:

- request ID
- HTTP method
- path without query string
- status code
- duration
- environment

Logs must not include report bodies, descriptions, tokens, exact locations, phone numbers, or
other personally identifying values. Use `LOG_FORMAT=json` for hosted environments and
`LOG_LEVEL=INFO` unless debugging a temporary non-production issue.

## Public Abuse Controls

`POST /v1/reports` has MVP guardrails for safer public launch:

- `MAX_REQUEST_BODY_BYTES` rejects oversized submissions before validation.
- `REPORT_RATE_LIMIT_COUNT` and `REPORT_RATE_LIMIT_WINDOW_SECONDS` throttle bursts from the
  same network client.
- Rate limiting is in-memory and intended as a first MVP layer. For multi-instance production,
  move this counter to Redis so limits apply consistently across API replicas.
- The limiter does not log or persist report text, phone numbers, exact location, or user identity.

## Worker Mode

For tests and simple local development, `CELERY_TASK_ALWAYS_EAGER=true` runs report processing
inside the API process. For a production-like local run, set `CELERY_TASK_ALWAYS_EAGER=false`
and start the Celery worker separately.

## Internal Review

Internal review endpoints require:

```text
X-Internal-Token: <INTERNAL_API_TOKEN>
```

In PostgreSQL mode, internal tokens are stored as SHA-256 hashes in the
`internal_api_keys` table. The request body cannot choose the reviewer identity;
review events use the reviewer attached to the authenticated key.

Use them to inspect reports marked `under_review` and apply safe review decisions:

- `aggregated`
- `closed`
- `unable_to_process`

These endpoints are intentionally not part of the citizen iPhone API surface.
Review decisions are stored in a dedicated `review_events` audit table.

## County Codes

County risk guidance uses Kenya county-code style identifiers:

```text
KE-001 Mombasa
KE-042 Kisumu
KE-047 Nairobi
```

## Important Safety Notes

- No user accounts are required.
- No phone number, email, national ID, or name is collected.
- Report text must not be sent to analytics.
- Push notifications must not include report content.
- Exact location is not required.
- In-memory storage is for development only.

## Next Implementation Milestones

1. Add PostGIS county centroids or boundaries for spatial aggregation.
2. Add role-scoped reviewer permissions beyond the default reviewer role.
3. Move public rate limiting to Redis for multi-instance deployments.
4. Add duplicate/spam controls for public report submission.
