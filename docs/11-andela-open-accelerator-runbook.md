# Andela x Open Accelerator Runbook

## Goal

Prepare the AmaniPulse Citizen iPhone app for accelerator demos, partner review, and controlled pilot readiness without weakening the safety posture of the MVP.

## Demo Mode

Use mock services for public walkthroughs unless a reviewed staging backend is available.

```bash
AMANIPULSE_API_PROFILE=mock
AMANIPULSE_DRAFT_STORE=in_memory
```

Demo script:

- Complete onboarding.
- Switch between English and Swahili.
- Start an anonymous report.
- Show the safety reminder and validation guidance.
- Submit with mock services and refresh status.
- Relaunch offline and show waiting-for-network recovery.

## Staging Mode

Use staging only after the accelerator space provides a confirmed HTTPS base URL.

```bash
AMANIPULSE_API_PROFILE=staging
AMANIPULSE_API_BASE_URL=https://<andela-open-accelerator-staging-host>
```

Staging acceptance checks:

- `POST /v1/reports` accepts an anonymous report payload.
- `GET /v1/reports/{reference}/status` returns a safe public status.
- `GET /v1/resources?language=en&country=KE` returns reviewed safety resources.
- `GET /v1/resources?language=sw&country=KE` returns reviewed Swahili resources.
- No account, device advertising ID, report analytics, or precise location is required.

## Accessibility Check

Run at least one simulator pass with accessibility text enabled:

```bash
AMANIPULSE_DYNAMIC_TYPE_SIZE=accessibility3
```

Minimum walkthrough:

- Onboarding remains readable.
- The report button remains reachable.
- Validation errors remain reachable and readable.
- Save draft remains reachable.
- Settings language control remains reachable.

## Safety Review

Before any live pilot:

- Confirm the app still states it is not an emergency response service.
- Confirm screenshots and demo recordings do not contain real reports.
- Confirm staging data is synthetic or approved for demo use.
- Confirm local drafts can be deleted from Settings.
- Confirm partner-facing claims do not imply AI certainty or emergency dispatch.
