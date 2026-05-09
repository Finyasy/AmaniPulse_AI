# Testing And Quality

## Quality Goal

The AmaniPulse AI iPhone MVP must be reliable, safe, accessible, and understandable under real field conditions. Quality is measured not only by technical correctness, but also by whether the app protects vulnerable users and works when connectivity is poor.

## Test Strategy

Testing should cover:

- Product behavior.
- Security and privacy.
- Offline reliability.
- Accessibility.
- Localization.
- API integration.
- AI output presentation boundaries.
- Field readiness.

## Unit Tests

Recommended coverage:

- Report validation.
- Incident category mapping.
- Location mode handling.
- Draft lifecycle state transitions.
- Consent validation.
- Localized content lookup.
- Risk level display mapping.
- Error message selection.
- Retry eligibility.

## UI Tests

Core UI scenarios:

- First launch onboarding.
- Language selection.
- Start report.
- Select category.
- Enter report details.
- Choose manual location.
- Submit report successfully.
- Save draft offline.
- Resume draft.
- Delete draft.
- View risk guidance.
- View resources.
- Change language in settings.

## Offline And Network Tests

Scenarios:

- Launch app without network.
- Start report without network.
- Save encrypted draft.
- Reopen app and recover draft.
- Attempt submission while offline.
- Submit after network returns.
- Backend returns retryable error.
- Backend returns validation error.
- Backend returns unsupported app version.
- Risk guidance unavailable.
- Cached resources displayed.

## Privacy Tests

Verify:

- No account is required.
- No report text appears in analytics.
- No report text appears in crash logs.
- No precise location is sent unless explicitly enabled.
- Draft deletion removes local draft data.
- Push notifications do not include report details.
- App previews do not expose sensitive report content where feasible.
- App Store privacy declarations match actual behavior.

## Security Tests

Verify:

- All API calls use HTTPS.
- App Transport Security is enabled.
- Drafts are encrypted at rest.
- Debug logs do not include report content.
- API errors are handled safely.
- Malformed server responses do not crash the app.
- Large text payloads are limited.
- Rate limit responses are handled gracefully.

## Accessibility Tests

Run tests with:

- VoiceOver.
- Dynamic Type accessibility sizes.
- Increased contrast.
- Reduced motion.
- Small iPhone screen.
- One-handed navigation.

Acceptance scenarios:

- VoiceOver user can complete a report.
- Large-text user can read all safety copy.
- Risk levels are understandable without color.
- Form errors are announced and visible.

## Localization Tests

Verify:

- English and Swahili strings are complete.
- No untranslated keys appear.
- Long translated strings do not break layout.
- Date and time formatting is local-aware.
- Incident category meanings remain clear.
- Safety disclaimers are accurate in both languages.

## AI And Risk Display Tests

The iPhone app should test presentation boundaries:

- Risk levels use calm language.
- No raw AI confidence score is shown to citizens.
- No alleged perpetrator names are displayed from AI outputs.
- Critical guidance does not create panic.
- Stale risk data shows a timestamp.
- No report-specific AI classification is exposed to the reporter unless approved by policy.

## Field Readiness Tests

Before pilot:

- Test with community representatives.
- Test with peacebuilding partners.
- Test in low-bandwidth environments.
- Test language comprehension.
- Test safety copy for misunderstanding.
- Test whether users understand that AmaniPulse is not an emergency service.
- Test whether users know when a report is saved versus submitted.

## Acceptance Checklist

- Citizen can report anonymously.
- Citizen can report without precise location.
- Citizen can save and delete offline drafts.
- Citizen can use English and Swahili.
- Citizen can access safety resources offline.
- App does not leak report content into logs, analytics, or notifications.
- App handles backend and network failure calmly.
- Accessibility basics pass before pilot.
- Partner review confirms risk guidance is safe and non-inflammatory.

## Release Gates

### Internal Alpha

- Core report flow works with mock APIs.
- Offline draft flow works.
- English copy complete.
- Basic privacy review complete.

### Partner Pilot

- Swahili localization complete.
- Backend staging APIs connected.
- Safety and moderation process defined.
- Accessibility testing complete.
- Partner resource content vetted.

### Public Launch

- Production backend available.
- Incident response process active.
- Monitoring configured.
- App Store privacy review complete.
- Data governance process approved.
- Community feedback loop established.
