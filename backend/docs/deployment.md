# Backend Deployment Runbook

This runbook covers the FastAPI backend only. The iPhone app, web dashboard, SMS,
USSD, and WhatsApp integrations are separate deployment surfaces.

## Production Runtime

Use the backend `Dockerfile` from the `backend/` directory:

```bash
docker build -t amanipulse-backend ./backend
docker run --rm -p 8000:8000 --env-file backend/.env amanipulse-backend
```

The container starts:

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --proxy-headers
```

## Required Production Environment

Set these values in the hosting provider secret manager, not in Git:

```text
ENVIRONMENT=production
STORAGE_BACKEND=postgres
DATABASE_URL=<postgresql+asyncpg production url>
REDIS_URL=<redis production url>
CELERY_TASK_ALWAYS_EAGER=false
REPORT_ENCRYPTION_KEY=<fernet key>
INTERNAL_API_TOKEN=<break-glass local-only token if memory mode is ever used>
LOG_LEVEL=INFO
LOG_FORMAT=json
REQUEST_ID_HEADER=X-Request-ID
MAX_REQUEST_BODY_BYTES=16000
REPORT_RATE_LIMIT_COUNT=12
REPORT_RATE_LIMIT_WINDOW_SECONDS=60
```

## Release Order

1. Build and deploy the API image.
2. Run database migrations once per release:

```bash
alembic upgrade head
```

3. Start the API web process.
4. Start the Celery worker process:

```bash
celery -A app.workers.celery_app.celery_app worker --loglevel=info
```

5. Verify readiness:

```bash
curl -fsS https://<api-host>/v1/ready
```

## Health Checks

Use `/v1/health` for liveness and `/v1/ready` for readiness.

In `STORAGE_BACKEND=postgres`, readiness checks database connectivity with `SELECT 1`.
If the database is unavailable, `/v1/ready` returns `503`.

## Safety Rules

- Do not log request bodies, report descriptions, internal tokens, phone numbers, or exact locations.
- Keep `LOG_FORMAT=json` in hosted environments.
- Rotate `REPORT_ENCRYPTION_KEY` through a planned migration only; changing it without re-encrypting reports prevents decrypting existing report descriptions.
- Disable any dev seeded internal token before a real pilot by issuing production reviewer keys and deactivating development keys in `internal_api_keys`.
- Keep public incident guidance calm and aggregate-only; never expose raw citizen reports from public endpoints.
