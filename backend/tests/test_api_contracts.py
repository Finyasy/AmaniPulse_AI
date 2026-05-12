from datetime import UTC, datetime, timedelta
from uuid import uuid4

import pytest
from fastapi.testclient import TestClient

from app.core.abuse import duplicate_report_guard, report_rate_limiter
from app.core.config import get_settings
from app.domain.counties import KENYA_COUNTY_RISK_SEEDS
from app.main import app, create_app

client = TestClient(app)


@pytest.fixture(autouse=True)
def reset_public_abuse_guards():
    report_rate_limiter.reset()
    duplicate_report_guard.reset()
    yield
    report_rate_limiter.reset()
    duplicate_report_guard.reset()


def test_health_check() -> None:
    response = client.get("/v1/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"
    assert response.json()["service"] == "amanipulse-api"
    assert response.json()["version"] == "0.1.0"


def test_readiness_check_uses_memory_storage_by_default() -> None:
    response = client.get("/v1/ready")
    assert response.status_code == 200
    assert response.json()["status"] == "ready"
    assert response.json()["checks"]["storage"] == "memory"


def test_request_id_header_is_preserved_or_generated() -> None:
    custom_response = client.get(
        "/v1/health",
        headers={"X-Request-ID": "ios-smoke-test-request"},
    )
    assert custom_response.status_code == 200
    assert custom_response.headers["X-Request-ID"] == "ios-smoke-test-request"

    generated_response = client.get("/v1/health")
    assert generated_response.status_code == 200
    assert generated_response.headers["X-Request-ID"]


def test_report_payload_size_limit_can_reject_large_public_submissions(monkeypatch) -> None:
    monkeypatch.setenv("MAX_REQUEST_BODY_BYTES", "200")
    get_settings.cache_clear()
    report_rate_limiter.reset()
    try:
        limited_client = TestClient(create_app())
        response = limited_client.post(
            "/v1/reports",
            json=_report_payload(f"oversize-{uuid4()}"),
        )
        assert response.status_code == 413
        assert response.json()["error"]["code"] == "payload_too_large"
    finally:
        get_settings.cache_clear()
        report_rate_limiter.reset()
        duplicate_report_guard.reset()


def test_report_rate_limit_throttles_public_submission_bursts(monkeypatch) -> None:
    monkeypatch.setenv("MAX_REQUEST_BODY_BYTES", "16000")
    monkeypatch.setenv("REPORT_RATE_LIMIT_COUNT", "1")
    monkeypatch.setenv("REPORT_RATE_LIMIT_WINDOW_SECONDS", "60")
    get_settings.cache_clear()
    report_rate_limiter.reset()
    try:
        limited_client = TestClient(create_app())
        first_response = limited_client.post(
            "/v1/reports",
            json=_report_payload(f"rate-first-{uuid4()}"),
        )
        assert first_response.status_code == 201

        second_response = limited_client.post(
            "/v1/reports",
            json=_report_payload(f"rate-second-{uuid4()}"),
        )
        assert second_response.status_code == 429
        assert second_response.json()["error"]["code"] == "rate_limited"
        assert second_response.headers["Retry-After"]
    finally:
        get_settings.cache_clear()
        report_rate_limiter.reset()
        duplicate_report_guard.reset()


def test_validation_errors_use_standard_error_shape() -> None:
    response = client.post(
        "/v1/reports",
        json={
            **_report_payload(f"invalid-{uuid4()}"),
            "source": "unknown_client",
        },
    )
    assert response.status_code == 422
    assert response.json()["error"]["code"] == "validation_error"


def test_web_citizen_portal_source_is_supported() -> None:
    response = client.post(
        "/v1/reports",
        json={
            **_report_payload(f"web-report-{uuid4()}"),
            "source": "web_citizen_portal",
        },
    )
    assert response.status_code == 201


def test_submit_report_and_fetch_status() -> None:
    payload = _report_payload("local-test-001")

    create_response = client.post("/v1/reports", json=payload)
    assert create_response.status_code == 201
    report_reference = create_response.json()["report_reference"]

    status_response = client.get(f"/v1/reports/{report_reference}/status")
    assert status_response.status_code == 200
    assert status_response.json()["report_reference"] == report_reference


def _report_payload(client_report_id: str) -> dict[str, object]:
    return {
        "client_report_id": client_report_id,
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


def test_risk_guidance() -> None:
    assert len(KENYA_COUNTY_RISK_SEEDS) == 47

    response = client.get("/v1/risk/county/KE-047")
    assert response.status_code == 200
    assert response.json()["county_name"] == "Nairobi"

    response = client.get("/v1/risk/county/KE-001")
    assert response.status_code == 200
    assert response.json()["county_name"] == "Mombasa"

    response = client.get("/v1/risk/county/KE-30")
    assert response.status_code == 404
    assert response.json()["error"]["code"] == "county_not_found"


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
    assert unauthorized.json()["error"]["code"] == "unauthorized"

    invalid = client.get(
        "/v1/internal/review/queue",
        headers={"X-Internal-Token": "not-the-review-token"},
    )
    assert invalid.status_code == 401
    assert invalid.json()["error"]["code"] == "unauthorized"

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
            "reviewer_id": "spoofed-reviewer",
            "note": "Included in aggregate monitoring.",
        },
    )
    assert decision_response.status_code == 200
    assert decision_response.json()["status"] == "aggregated"
    assert decision_response.json()["reviewer_id"] == "dev-reviewer"

    events_response = client.get(
        f"/v1/internal/review/reports/{report_reference}/events",
        headers=headers,
    )
    assert events_response.status_code == 200
    events = events_response.json()["events"]
    assert len(events) == 1
    assert events[0]["previous_status"] == "under_review"
    assert events[0]["new_status"] == "aggregated"
    assert events[0]["reviewer_id"] == "dev-reviewer"

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
    assert labels["recommended_action"] == "human_review"
    assert labels["review_priority"] == "high"
    assert "person@example.com" not in labels["safety_flags"]
    assert "+254712345678" not in labels["safety_flags"]


def test_decision_intelligence_outputs_richer_review_labels() -> None:
    payload = {
        **_report_payload(f"decision-{uuid4()}"),
        "category": "violence_threat",
        "description": "People are threatening an armed attack near a rally.",
    }
    create_response = client.post("/v1/reports", json=payload)
    assert create_response.status_code == 201
    report_reference = create_response.json()["report_reference"]

    detail_response = client.get(
        f"/v1/internal/review/reports/{report_reference}",
        headers={"X-Internal-Token": "dev-internal-review-token"},
    )
    assert detail_response.status_code == 200
    labels = detail_response.json()["ai_labels"]
    assert labels["model_version"] == "decision-rules-mvp-0.2"
    assert labels["risk_score"] >= labels["severity_score"]
    assert labels["confidence"] > 0
    assert labels["review_priority"] in {"high", "critical"}
    assert labels["recommended_action"] in {"human_review", "urgent_human_review"}
    assert labels["public_guidance_allowed"] is False
    assert "escalation_language" in labels["risk_factors"]


def test_duplicate_report_signal_routes_repeat_submission_to_review() -> None:
    duplicate_report_guard.reset()
    try:
        first_payload = _report_payload(f"dup-first-{uuid4()}")
        second_payload = {
            **first_payload,
            "client_report_id": f"dup-second-{uuid4()}",
        }

        first_response = client.post("/v1/reports", json=first_payload)
        assert first_response.status_code == 201
        second_response = client.post("/v1/reports", json=second_payload)
        assert second_response.status_code == 201

        report_reference = second_response.json()["report_reference"]
        detail_response = client.get(
            f"/v1/internal/review/reports/{report_reference}",
            headers={"X-Internal-Token": "dev-internal-review-token"},
        )
        assert detail_response.status_code == 200
        assert detail_response.json()["status"] == "under_review"
        labels = detail_response.json()["ai_labels"]
        assert labels["duplicate_signal"] is True
        assert labels["recommended_action"] == "review_duplicate_before_aggregation"
        assert labels["public_guidance_allowed"] is False
        assert "possible_duplicate_or_spam" in labels["risk_factors"]
    finally:
        duplicate_report_guard.reset()
