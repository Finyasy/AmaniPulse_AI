# Technical Architecture

## Architecture Goal

Build a secure, resilient Native SwiftUI iPhone app that supports anonymous reporting, offline drafting, multilingual content, and low-bandwidth integration with the broader AmaniPulse AI platform.

## Recommended iOS Stack

- **UI:** SwiftUI.
- **State management:** Swift Observation or a lightweight observable state layer.
- **Concurrency:** Swift structured concurrency with async/await.
- **Persistence:** encrypted local storage for drafts and app configuration.
- **Networking:** URLSession with retry policies and request timeouts.
- **Localization:** native iOS localization strings and remotely configurable content.
- **Testing:** XCTest, XCUITest, accessibility audits, and privacy-focused integration tests.

## App Layers

### Presentation Layer

SwiftUI views for onboarding, reporting, risk guidance, resources, and settings. Views should remain mostly declarative and avoid direct networking or persistence logic.

### Domain Layer

Pure Swift models and use cases for:

- Creating a report draft.
- Validating report fields.
- Redacting risky personal information hints.
- Preparing submission payloads.
- Loading risk guidance.
- Managing language and configuration.

### Data Layer

Services for:

- API communication.
- Local encrypted draft storage.
- Remote configuration caching.
- Resource content caching.
- Connectivity detection.
- Submission retry orchestration.

## Recommended Module Boundaries

- `Reporting`: report form, draft lifecycle, submission, report status.
- `RiskGuidance`: county risk levels, public guidance, risk explanation.
- `Resources`: static and remote safety resources.
- `PrivacySafety`: consent, redaction hints, local data controls.
- `Localization`: language preferences and content lookup.
- `CoreNetworking`: API client, request signing if needed, retries.
- `CoreStorage`: encrypted local persistence.

## Data Flow

1. User creates a report draft in the Report flow.
2. Draft is validated locally.
3. Draft is encrypted and stored on device until submission succeeds or the user deletes it.
4. On submission, the app sends a minimal anonymous payload to the backend.
5. Backend returns a non-identifying report reference and status.
6. The app stores only the reference, status, and local draft metadata.
7. Aggregated backend services classify the report and update regional risk intelligence.

## Backend Integration Assumptions

The iPhone app integrates with platform APIs for:

- Report submission.
- Incident taxonomy.
- County risk guidance.
- App configuration.
- Localized resource content.
- Optional report status lookup by anonymous reference.

The app must not require backend user accounts, session profiles, phone verification, or identity binding.

## Offline Strategy

The app should support offline-first report drafting:

- Drafts are created locally before network submission.
- Drafts are encrypted at rest.
- Draft status clearly indicates whether submission occurred.
- Retry behavior is transparent.
- Draft deletion is always available.
- Remote resources and risk guidance are cached with timestamps.

Bundled safety resources should be available even on first launch without network.

## Push Notification Strategy

Push notifications are optional and should be disabled by default until the user opts in.

Notifications may support:

- Generic report status updates.
- Generic public safety guidance updates.

Notifications must not contain:

- Incident details.
- Report categories.
- Precise locations.
- Political or ethnic group references.
- Language that identifies the user as a reporter.

## Analytics Boundaries

Analytics should be privacy-preserving and minimal.

Allowed:

- Anonymous event counts.
- Screen completion rates.
- Network error rates.
- Language selection counts.
- Crash diagnostics without report content.

Not allowed:

- Report text in analytics.
- Exact location in analytics.
- Persistent user identity.
- Device fingerprinting for tracking.
- Cross-app advertising identifiers.

## Deployment Environments

Recommended environments:

- **Development:** local and internal testing with mock APIs.
- **Staging:** realistic API behavior with synthetic data.
- **Pilot:** limited partner/community deployment with safety monitoring.
- **Production:** App Store release with vetted backend, incident response process, and monitoring.

## Security Architecture

- Use TLS for all network traffic.
- Store drafts with strong local encryption.
- Avoid logging report content.
- Avoid storing access tokens tied to user identity.
- Use app transport security.
- Protect secrets through backend-mediated configuration, not hardcoded client secrets.
- Limit cached risk data to aggregated, non-sensitive information.

## Failure Handling

- If report submission fails, keep the draft local and visible to the user.
- If risk guidance fails, show cached guidance with timestamp or an unavailable state.
- If localization content fails, use bundled strings.
- If configuration fails, use safe defaults.
- If the app detects degraded network, reduce non-essential requests.

## Engineering Standards

- Use feature flags for risky or pilot-only capabilities.
- Treat privacy requirements as acceptance criteria.
- Keep UI copy centralized for localization review.
- Prefer small, testable domain services over view-heavy logic.
- Use dependency injection for API and storage services.
- Maintain synthetic test data for demos and staging.
