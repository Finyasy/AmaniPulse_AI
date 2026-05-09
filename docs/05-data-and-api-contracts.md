# Data And API Contracts

## Purpose

This document defines conceptual API contracts for the AmaniPulse AI iPhone Citizen MVP. These contracts are implementation guidance, not final backend schemas.

All interfaces should preserve anonymity, minimize personal data, and avoid collecting more information than needed for peacebuilding analysis.

## General API Principles

- Use HTTPS for all requests.
- Do not require a user account or login token.
- Do not include device advertising identifiers.
- Do not send report content to analytics services.
- Prefer short payloads and compression-friendly JSON.
- Return clear machine-readable error codes.
- Include localized display content through configuration where practical.

## Incident Taxonomy

MVP categories:

```json
[
  "violence_threat",
  "active_violence",
  "voter_intimidation",
  "hate_speech_or_incitement",
  "misinformation_or_rumor",
  "corruption_bribery_or_coercion",
  "authority_abuse",
  "suspicious_mobilization",
  "other_election_safety_concern"
]
```

Each category should have:

- Stable ID.
- Localized name.
- Localized short description.
- Optional category-specific prompts.
- Safety guidance snippet.

## Report Submission

Endpoint:

```text
POST /v1/reports
```

Example request:

```json
{
  "client_report_id": "local-uuid",
  "category": "voter_intimidation",
  "description": "People are being warned not to attend a local registration event.",
  "incident_time": "2026-05-09T08:30:00Z",
  "location": {
    "mode": "manual_area",
    "country": "KE",
    "county": "Nairobi",
    "area_label": "Kasarani"
  },
  "language": "en",
  "source": "ios_citizen_app",
  "app_version": "1.0.0",
  "consents": {
    "anonymous_submission": true,
    "risk_analysis": true
  }
}
```

Example response:

```json
{
  "report_reference": "AP-2027-8F3KQ2",
  "status": "received",
  "received_at": "2026-05-09T08:31:12Z",
  "message": "Your anonymous report was received."
}
```

## Location Object

Supported location modes:

```json
{
  "mode": "none"
}
```

```json
{
  "mode": "manual_area",
  "country": "KE",
  "county": "Kisumu",
  "area_label": "Ahero"
}
```

```json
{
  "mode": "approximate_coordinates",
  "country": "KE",
  "county": "Mombasa",
  "latitude_rounded": -4.05,
  "longitude_rounded": 39.66,
  "precision_km": 5
}
```

Precise coordinates should not be required for MVP reporting.

## Report Status

Endpoint:

```text
GET /v1/reports/{report_reference}/status
```

Example response:

```json
{
  "report_reference": "AP-2027-8F3KQ2",
  "status": "under_review",
  "updated_at": "2026-05-09T09:10:00Z",
  "display_message": "Your report has been received and is being reviewed."
}
```

Allowed statuses:

- `received`
- `under_review`
- `aggregated`
- `closed`
- `unable_to_process`

The app should not display sensitive moderation notes.

## County Risk Guidance

Endpoint:

```text
GET /v1/risk/county/{county_code}
```

Example response:

```json
{
  "county_code": "KE-30",
  "county_name": "Nairobi",
  "risk_level": "moderate",
  "score": 54,
  "updated_at": "2026-05-09T07:00:00Z",
  "summary": "Community reports and public signals suggest elevated tension in some areas.",
  "guidance": [
    "Avoid sharing unverified claims.",
    "Move away from crowds if tensions rise.",
    "Use anonymous reporting if you witness intimidation."
  ]
}
```

Risk levels:

- `low`
- `moderate`
- `high`
- `critical`

Risk language must be calm, non-partisan, and non-accusatory.

## App Configuration

Endpoint:

```text
GET /v1/app-config?platform=ios&version=1.0.0&language=en
```

Example response:

```json
{
  "minimum_supported_version": "1.0.0",
  "feature_flags": {
    "media_uploads": false,
    "push_notifications": false,
    "report_status_lookup": true
  },
  "emergency_disclaimer": "AmaniPulse is not an emergency response service.",
  "support_channels": {
    "sms": "TBD",
    "ussd": "TBD",
    "whatsapp": "TBD"
  }
}
```

## Localized Resources

Endpoint:

```text
GET /v1/resources?language=sw&country=KE
```

Example response:

```json
{
  "language": "sw",
  "resources": [
    {
      "id": "digital-safety",
      "title": "Usalama wa kidijitali",
      "body": "Epuka kusambaza taarifa ambazo hujathibitisha.",
      "category": "digital_safety",
      "updated_at": "2026-05-09T07:00:00Z"
    }
  ]
}
```

Resources should be cacheable and safe to bundle offline.

## Error Shape

Example response:

```json
{
  "error": {
    "code": "network_unavailable",
    "message": "The report could not be submitted right now.",
    "retryable": true
  }
}
```

Recommended error codes:

- `validation_failed`
- `network_unavailable`
- `service_unavailable`
- `rate_limited`
- `unsupported_app_version`
- `content_too_large`
- `unable_to_process`

## Client-Side Data Retention

The app should store:

- Encrypted unsubmitted drafts.
- Submission reference and non-sensitive status.
- Cached resources.
- Cached county risk guidance.
- Language preference.
- Feature flags.

The app should not store:

- User identity.
- Phone number.
- National ID.
- Precise location history.
- Raw server moderation notes.
- Report content after successful submission unless the user explicitly saved it as a local copy.
