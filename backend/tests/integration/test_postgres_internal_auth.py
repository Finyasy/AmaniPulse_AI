import os
from datetime import UTC, datetime, timedelta
from uuid import uuid4

import pytest
from fastapi.testclient import TestClient

from app.main import app

pytestmark = pytest.mark.skipif(
    os.getenv("RUN_POSTGRES_TESTS") != "1",
    reason="Postgres integration tests require RUN_POSTGRES_TESTS=1",
)

client = TestClient(app)


def test_postgres_readiness_checks_database() -> None:
    response = client.get("/v1/ready")
    assert response.status_code == 200
    assert response.json()["status"] == "ready"
    assert response.json()["checks"]["storage"] == "postgres"
    assert response.json()["checks"]["database"] == "ok"


def test_postgres_internal_review_uses_hashed_api_key_identity() -> None:
    client_report_id = f"pg-review-{uuid4()}"
    create_response = client.post(
        "/v1/reports",
        json={
            "client_report_id": client_report_id,
            "category": "violence_threat",
            "description": "A group is warning people about an attack near a public rally.",
            "incident_time": (datetime.now(UTC) - timedelta(minutes=5)).isoformat(),
            "location": {
                "mode": "manual_area",
                "country": "KE",
                "county": "Nairobi",
                "area_label": "Kasarani",
            },
            "language": "en",
            "source": "ios_citizen_app",
            "app_version": "1.0.0",
            "consents": {
                "anonymous_submission": True,
                "risk_analysis": True,
            },
        },
    )
    assert create_response.status_code == 201
    report_reference = create_response.json()["report_reference"]

    invalid_response = client.get(
        "/v1/internal/review/queue",
        headers={"X-Internal-Token": "invalid-token"},
    )
    assert invalid_response.status_code == 401

    headers = {"X-Internal-Token": "dev-internal-review-token"}
    decision_response = client.post(
        f"/v1/internal/review/reports/{report_reference}/decision",
        headers=headers,
        json={
            "status": "aggregated",
            "reviewer_id": "spoofed-reviewer",
            "note": "Confirmed for aggregate monitoring only.",
        },
    )
    assert decision_response.status_code == 200
    assert decision_response.json()["reviewer_id"] == "dev-reviewer"

    events_response = client.get(
        f"/v1/internal/review/reports/{report_reference}/events",
        headers=headers,
    )
    assert events_response.status_code == 200
    assert events_response.json()["events"][0]["reviewer_id"] == "dev-reviewer"
