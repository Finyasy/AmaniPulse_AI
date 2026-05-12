#!/usr/bin/env python3
"""Smoke-check an AmaniPulse staging backend with synthetic MVP data."""

from __future__ import annotations

import argparse
import json
import sys
from datetime import UTC, datetime, timedelta
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen
from uuid import uuid4


def request_json(
    base_url: str,
    path: str,
    *,
    method: str = "GET",
    payload: dict[str, Any] | None = None,
    query: dict[str, str] | None = None,
) -> tuple[int, dict[str, Any]]:
    url = f"{base_url.rstrip('/')}{path}"
    if query:
        url = f"{url}?{urlencode(query)}"

    body = None
    headers = {"Accept": "application/json"}
    if payload is not None:
        body = json.dumps(payload).encode("utf-8")
        headers["Content-Type"] = "application/json"

    request = Request(url, data=body, headers=headers, method=method)
    try:
        with urlopen(request, timeout=15) as response:
            data = response.read().decode("utf-8")
            return response.status, json.loads(data)
    except HTTPError as error:
        data = error.read().decode("utf-8")
        try:
            parsed = json.loads(data)
        except json.JSONDecodeError:
            parsed = {"error": data}
        return error.code, parsed
    except URLError as error:
        raise RuntimeError(f"Could not reach {url}: {error.reason}") from error


def assert_status(actual: int, expected: int, label: str) -> None:
    if actual != expected:
        raise AssertionError(f"{label} expected HTTP {expected}, got HTTP {actual}")


def synthetic_report() -> dict[str, Any]:
    return {
        "client_report_id": f"smoke-{uuid4()}",
        "category": "voter_intimidation",
        "description": "Synthetic staging smoke test report. Do not use for real review.",
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


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("base_url", help="Staging API base URL, for example https://staging.example.com")
    args = parser.parse_args()

    checks: list[str] = []

    status, health = request_json(args.base_url, "/v1/health")
    assert_status(status, 200, "health")
    checks.append(f"health={health.get('status', 'unknown')}")

    status, config = request_json(
        args.base_url,
        "/v1/app-config",
        query={"platform": "ios", "version": "1.0.0", "language": "en"},
    )
    assert_status(status, 200, "app configuration")
    if "report_status_lookup" not in config.get("feature_flags", {}):
        raise AssertionError("app configuration is missing report_status_lookup feature flag")
    checks.append("app-config")

    status, taxonomy = request_json(args.base_url, "/v1/incident-taxonomy", query={"language": "sw"})
    assert_status(status, 200, "Swahili incident taxonomy")
    if taxonomy.get("language") != "sw" or not taxonomy.get("categories"):
        raise AssertionError("Swahili taxonomy response is incomplete")
    checks.append("taxonomy-sw")

    status, resources = request_json(args.base_url, "/v1/resources", query={"language": "sw", "country": "KE"})
    assert_status(status, 200, "Swahili resources")
    if resources.get("language") != "sw" or not resources.get("resources"):
        raise AssertionError("Swahili resources response is incomplete")
    checks.append("resources-sw")

    status, risk = request_json(args.base_url, "/v1/risk/county/KE-047")
    assert_status(status, 200, "Nairobi risk guidance")
    if risk.get("county_name") != "Nairobi":
        raise AssertionError("Nairobi risk guidance returned the wrong county")
    checks.append("risk-nairobi")

    status, receipt = request_json(args.base_url, "/v1/reports", method="POST", payload=synthetic_report())
    assert_status(status, 201, "report submission")
    report_reference = receipt.get("report_reference")
    if not report_reference:
        raise AssertionError("report receipt is missing report_reference")
    checks.append(f"report={report_reference}")

    status, report_status = request_json(args.base_url, f"/v1/reports/{report_reference}/status")
    assert_status(status, 200, "report status")
    if report_status.get("report_reference") != report_reference:
        raise AssertionError("report status returned a different report_reference")
    checks.append(f"status={report_status.get('status', 'unknown')}")

    print("AmaniPulse staging smoke passed:")
    for check in checks:
        print(f"- {check}")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as error:
        print(f"AmaniPulse staging smoke failed: {error}", file=sys.stderr)
        raise SystemExit(1)
