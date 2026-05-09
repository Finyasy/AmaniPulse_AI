from datetime import UTC, datetime, timedelta

from fastapi.testclient import TestClient

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
    response = client.get("/v1/risk/county/KE-30")
    assert response.status_code == 200
    assert response.json()["county_name"] == "Nairobi"


def test_taxonomy_supports_swahili() -> None:
    response = client.get("/v1/incident-taxonomy?language=sw")
    assert response.status_code == 200
    assert response.json()["language"] == "sw"
    assert len(response.json()["categories"]) > 0
