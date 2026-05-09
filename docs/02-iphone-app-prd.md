# iPhone App PRD

## Product

AmaniPulse AI iPhone Citizen MVP

## Platform

Native iOS application built with SwiftUI.

## Objective

Provide a safe, anonymous, multilingual, low-bandwidth iPhone reporting experience for citizens during the 2027 Kenya General Elections.

## MVP Users

The MVP is designed for citizens and community members. It is not designed for NGO operators, analysts, moderators, or election observers performing triage.

## Core Use Cases

- Report a violence threat.
- Report voter intimidation.
- Report corruption, bribery, or coercion.
- Report hate speech or incitement.
- Report misinformation or rumor escalation.
- Report a general safety concern related to election tension.
- Save a report offline and submit later.
- Access guidance on staying safe.
- Check local public risk guidance without exposing identity.

## MVP Feature Set

### 1. Anonymous Onboarding

The app opens with a short explanation of:

- What AmaniPulse AI does.
- What can be reported.
- What anonymity means.
- What data may still be collected for safety and analysis.
- What the app cannot guarantee.

No account creation is allowed in the MVP.

### 2. Language Selection

The user can choose English or Swahili during onboarding. The app should also respect the iOS preferred language where possible.

Language can be changed later from settings.

### 3. Incident Category Selection

Supported MVP categories:

- Violence threat.
- Active violence or unrest.
- Voter intimidation.
- Hate speech or incitement.
- Misinformation or rumor.
- Corruption, bribery, or coercion.
- Police or authority abuse.
- Suspicious mobilization.
- Other election safety concern.

Each category should include a short plain-language description.

### 4. Report Details

The report form should support:

- Free-text description.
- Optional media attachment, disabled by default until safety review is complete.
- Incident time selection.
- Location option.
- Optional contact preference, disabled by default for strict anonymity in MVP.
- Safety confirmation before submission.

Free text must warn users not to include names, phone numbers, exact home addresses, or other personally identifying information unless absolutely necessary.

### 5. Location Consent

The user chooses one of:

- Use approximate current location.
- Choose county or area manually.
- Submit without location.

Precise GPS should not be the default. If enabled later, it must require explicit consent and explain risk.

### 6. Offline Drafts

If the user loses connectivity, the app should:

- Save the draft locally in encrypted storage.
- Clearly indicate that the report has not yet been submitted.
- Retry only after user confirmation or according to a transparent retry setting.
- Allow deleting drafts at any time.

### 7. Submission Confirmation

After successful submission, the app shows:

- A non-identifying report reference.
- A safety reminder.
- A note that reports may be aggregated and reviewed.
- An explanation that submitting a report does not guarantee emergency response.

### 8. Report Status

The MVP may show local status only:

- Draft.
- Waiting for network.
- Submitted.
- Received.
- Under review.

Status updates must not reveal sensitive investigation details.

### 9. Local Risk Guidance

The app may show county-level risk guidance such as Low, Moderate, High, or Critical. This should be framed as public safety awareness, not a prediction guarantee.

Risk guidance should avoid inflammatory language and should never identify individual reporters.

### 10. Trusted Resources

The app includes static or remotely configurable resources:

- Emergency safety guidance.
- Digital safety tips.
- How to de-escalate rumors.
- Contact information for vetted partner organizations where appropriate.
- Instructions for using SMS, USSD, or WhatsApp channels if available.

## Out Of Scope For MVP

- User accounts.
- Public social feeds.
- Direct messaging between citizens.
- Live chat with responders.
- Responder dashboard.
- Case management.
- Law enforcement dispatch.
- Identity verification.
- In-app political discussion forums.
- Publishing raw reports publicly.
- Showing exact incident reporter locations.

## Functional Requirements

- The user can complete a report in under 90 seconds for common incidents.
- The user can submit without creating an account.
- The user can submit without sharing precise location.
- The user can recover from network failure without losing report content.
- The user can change app language.
- The user can read safety guidance without logging in.
- The app can receive app configuration from backend services.
- The app can display remote incident categories and resource content.

## Non-Functional Requirements

- Report drafts are encrypted on device.
- Network payloads are encrypted in transit.
- The app minimizes background network activity.
- The app supports VoiceOver and Dynamic Type.
- The app remains usable on low bandwidth.
- The app avoids dark patterns around consent.
- The app uses plain language and culturally appropriate copy.
- The app handles server failure gracefully.

## Safety Requirements

- Do not promise emergency rescue.
- Do not ask for names, ID numbers, or phone numbers.
- Do not expose report content in push notifications.
- Do not show sensitive details on the lock screen.
- Do not display exact reporter location back to the user after submission.
- Do not allow screenshots of particularly sensitive confirmation screens if iOS controls are feasible.

## Acceptance Criteria

- A first-time user can understand the app purpose and anonymity model before reporting.
- A user can submit a report with category, description, time, and manual location.
- A user can submit a report without location.
- A user can save a report while offline and submit when online.
- A user can delete an unsubmitted draft.
- A user can switch between English and Swahili.
- A user can access safety resources without submitting a report.
- A user never needs an account to report.
