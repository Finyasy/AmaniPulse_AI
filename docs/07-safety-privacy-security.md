# Safety, Privacy, And Security

## Safety Goal

AmaniPulse AI must protect vulnerable users before it protects data quality. The iPhone app should reduce reporting risk, avoid unnecessary collection, and make the limits of anonymity understandable.

## Anonymity Model

The MVP should not require:

- Name.
- Phone number.
- Email address.
- National ID.
- Account registration.
- Social login.
- Profile photo.
- Persistent public username.

The app may still transmit technical metadata needed for security and service operation. Any such metadata must be minimized, documented, and separated from report content where possible.

## Anonymity Copy

The app should say:

> You do not need an account to report. Avoid including your name, phone number, exact home address, or other personal details in your report.

The app should not say:

> You are completely untraceable.

Absolute anonymity claims are unsafe because network, device, legal, and operational risks can vary.

## Data Minimization

Collect only:

- Incident category.
- Description.
- Incident time.
- Optional approximate or manual location.
- Language.
- Consent flags.
- App version.
- Anonymous local report ID.

Avoid collecting:

- Contact details.
- Exact location by default.
- Device advertising identifiers.
- Address book access.
- Photo library access unless media uploads are explicitly enabled later.
- Background location.
- Cross-app tracking identifiers.

## Local Data Protection

The app should:

- Encrypt drafts at rest.
- Allow users to delete unsubmitted drafts.
- Avoid storing submitted report content unless needed for local status.
- Hide sensitive content from app previews where feasible.
- Avoid logging report content.
- Respect iOS privacy controls.

## Network Security

- Use HTTPS with modern TLS.
- Enforce App Transport Security.
- Use short request timeouts and safe retries.
- Avoid sending data to third-party analytics.
- Avoid hardcoded backend secrets.
- Treat all backend responses as untrusted input.

## Consent

Consent should be specific and understandable:

- Anonymous report submission.
- Optional approximate location sharing.
- Use of report content for conflict risk analysis.
- Optional push notifications.

Consent must not be bundled into a single confusing checkbox.

## Location Safety

Default location behavior should be conservative:

- Manual county or area selection should be available.
- Approximate location should be explained before use.
- Precise location should not be required.
- Background location should not be used.
- Location should not appear in lock-screen notifications.

## Abuse Prevention

The platform must expect bad actors. Abuse controls may include:

- Rate limiting.
- Duplicate detection.
- Spam classification.
- Human moderation queues.
- Device-level abuse signals that do not become user tracking.
- Safe blocking of malicious payloads.
- Server-side validation.

Abuse prevention should not undermine anonymity for legitimate vulnerable users.

## Moderation

Human moderation should be used for:

- Imminent threats.
- Named individuals.
- Hate speech ambiguity.
- Possible false reporting campaigns.
- High-severity escalation signals.
- Media attachments if enabled later.

Moderators should see only the data needed for review.

## Legal And Ethical Risks

Risks to manage:

- Retaliation if a reporter is identified.
- Misuse of reports for political targeting.
- Overreliance on AI predictions.
- Defamation risk from unverified allegations.
- Government or institutional pressure for raw data.
- Underreporting from communities with lower smartphone access.
- False reports designed to create panic.

The platform should have a governance process for data requests, partner access, moderation policy, and emergency escalation.

## Vulnerable-User Protections

The app should:

- Remind users to move to safety before reporting.
- Avoid asking users to collect evidence in dangerous situations.
- Provide non-sensitive resources.
- Avoid exposing report activity in notifications.
- Allow local draft deletion.
- Explain that reporting is optional.
- Use calm, non-alarming language.

## Security Review Checklist

- No account required for MVP reporting.
- No precise location required.
- No report content in analytics.
- No report content in crash logs.
- No sensitive push notification text.
- Drafts encrypted at rest.
- Draft deletion tested.
- API errors do not leak sensitive data.
- Debug logging disabled in production.
- App Store privacy labels match actual behavior.

## Incident Response

Before pilot launch, the team should define:

- Who can access reports.
- Who reviews critical reports.
- How partner escalation works.
- How false reports are handled.
- How data breaches are reported.
- How backend access is audited.
- How app users are protected if risk increases.

## Privacy Promise

AmaniPulse AI should communicate a simple promise:

> We collect the least information needed to help identify peace and safety risks. You can report without an account, control location sharing, and delete drafts that have not been submitted.
