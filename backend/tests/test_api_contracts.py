from datetime import UTC, datetime, timedelta

from fastapi.testclient import TestClient

from app.domain.counties import KENYA_COUNTY_RISK_SEEDS
from app.main import app

client = TestClient(app)


def test_health_check() -> None:
    response = client.get("/v1/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_submit_report_and_fetch_status() -> None:
    payload = {
        "client_report_id": "local-test-001",
        "category": "voter_intimidation",
        "description": "People are being warned not to attend a registration event.",
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
    }

    create_response = client.post("/v1/reports", json=payload)
    assert create_response.status_code == 201
    report_reference = create_response.json()["report_reference"]

    status_response = client.get(f"/v1/reports/{report_reference}/status")
    assert status_response.status_code == 200
    assert status_response.json()["report_reference"] == report_reference


def test_risk_guidance() -> None:
    assert len(KENYA_COUNTY_RISK_SEEDS) == 47

    response = client.get("/v1/risk/county/KE-047")
    assert response.status_code == 200
    assert response.json()["county_name"] == "Nairobi"

    response = client.get("/v1/risk/county/KE-001")
    assert response.status_code == 200
    assert response.json()["county_name"] == "Mombasa"


def test_taxonomy_supports_swahili() -> None:
    response = client.get("/v1/incident-taxonomy?language=sw")
    assert response.status_code == 200
    assert response.json()["language"] == "sw"
    assert len(response.json()["categories"]) > 0


def test_internal_review_flow_requires_token_and_applies_decision() -> None:
    payload = {
        "client_report_id": "local-review-001",
        "category": "violence_threat",
        "description": "A group is warning people about an attack near a rally.",
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
    }

    create_response = client.post("/v1/reports", json=payload)
    assert create_response.status_code == 201
    report_reference = create_response.json()["report_reference"]

    unauthorized = client.get("/v1/internal/review/queue")
    assert unauthorized.status_code == 401

    headers = {"X-Internal-Token": "dev-internal-review-token"}
    queue_response = client.get("/v1/internal/review/queue", headers=headers)
    assert queue_response.status_code == 200
    references = [item["report_reference"] for item in queue_response.json()["reports"]]
    assert report_reference in references

    detail_response = client.get(
        f"/v1/internal/review/reports/{report_reference}",
        headers=headers,
    )
    assert detail_response.status_code == 200
    assert "attack near a rally" in detail_response.json()["description"]

    decision_response = client.post(
        f"/v1/internal/review/reports/{report_reference}/decision",
        headers=headers,
        json={
            "status": "aggregated",
            "reviewer_id": "reviewer-1",
            "note": "Included in aggregate monitoring.",
        },
    )
    assert decision_response.status_code == 200
    assert decision_response.json()["status"] == "aggregated"

    events_response = client.get(
        f"/v1/internal/review/reports/{report_reference}/events",
        headers=headers,
    )
    assert events_response.status_code == 200
    events = events_response.json()["events"]
    assert len(events) == 1
    assert events[0]["previous_status"] == "under_review"
    assert events[0]["new_status"] == "aggregated"
    assert events[0]["reviewer_id"] == "reviewer-1"

    status_response = client.get(f"/v1/reports/{report_reference}/status")
    assert status_response.status_code == 200
    assert status_response.json()["status"] == "aggregated"


def test_pii_hints_move_report_to_review_without_exposing_values() -> None:
    payload = {
        "client_report_id": "local-pii-001",
        "category": "misinformation_or_rumor",
        "description": "A rumor includes person@example.com and +254712345678.",
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
    }

    create_response = client.post("/v1/reports", json=payload)
    assert create_response.status_code == 201
    report_reference = create_response.json()["report_reference"]

    headers = {"X-Internal-Token": "dev-internal-review-token"}
    detail_response = client.get(
        f"/v1/internal/review/reports/{report_reference}",
        headers=headers,
    )
    assert detail_response.status_code == 200
    labels = detail_response.json()["ai_labels"]
    assert labels["pii_detected"] is True
    assert labels["safety_flags"] == "email,phone_number"
    assert "person@example.com" not in labels["safety_flags"]
    assert "+254712345678" not in labels["safety_flags"]
