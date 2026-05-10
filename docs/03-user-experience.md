# User Experience

## UX Goal

The iPhone app should feel calm, trustworthy, fast, and safe. It must support people who may be frightened, under time pressure, using limited data, or unsure whether reporting could expose them to retaliation.

The design should avoid sensational visuals, political cues, aggressive alerts, or language that increases panic.

## Experience Principles

- **Safety first:** every screen should reduce risk and avoid unnecessary disclosure.
- **Plain language:** use direct words that work across literacy levels.
- **Fast reporting:** the primary path should require minimal typing.
- **Consent clarity:** explain what is optional, what is required, and why.
- **Low cognitive load:** avoid dense forms and legalistic copy.
- **No shame, no blame:** users should never feel responsible for solving the incident.
- **Actionable calm:** guidance should help users take safe next steps without panic.

## Core Navigation

Recommended MVP tab structure:

- **Report:** start or continue an anonymous incident report.
- **Risk:** view county-level safety guidance and public risk levels.
- **Resources:** access safety, digital hygiene, and reporting guidance.
- **Settings:** language, privacy, draft management, and app information.

The Report tab should be the default landing destination after onboarding.

## First Launch Flow

1. Welcome screen explains AmaniPulse AI in one short paragraph.
2. Safety promise explains anonymous reporting and data minimization.
3. Limits screen explains that the app is not an emergency service.
4. Language selection offers English and Swahili.
5. Optional location education explains approximate/manual/no-location choices.
6. User lands on the Report screen.

## Report Flow

1. Choose incident category.
2. Add short description.
3. Choose when it happened.
4. Choose location sharing option.
5. Review safety reminder.
6. Submit or save draft.
7. View confirmation.

The user should be able to back out without losing progress.

## Screen Map

### Welcome

Purpose: establish trust, mission, and safety.

Content:

- Short value proposition.
- "Report anonymously" emphasis.
- "Continue" action.

### Safety Promise

Purpose: explain anonymity without overpromising.

Content:

- No account required.
- Do not include personal details.
- Location sharing is optional.
- Reports may be reviewed and aggregated.

### Report Start

Purpose: let users begin quickly.

Content:

- Primary "Report an incident" button.
- Continue draft card if one exists.
- Emergency disclaimer.

### Category Picker

Purpose: classify the report with minimal effort.

Content:

- Incident categories with descriptions.
- "Not sure" or "Other" option.

### Report Details

Purpose: collect enough context for triage.

Content:

- Text area with safety hints.
- Incident time selector.
- Optional structured prompts based on category.

### Location Choice

Purpose: collect useful geographic context safely.

Content:

- Approximate current location.
- Manual county or area.
- No location.
- Explanation of tradeoffs.

### Review And Submit

Purpose: prevent accidental disclosure.

Content:

- Report summary.
- Personal information warning.
- Consent checkbox.
- Submit button.
- Save draft option.

### Confirmation

Purpose: reassure the user and set expectations.

Content:

- Report reference.
- Status.
- Safety reminder.
- "Close" action.

### Risk

Purpose: provide non-sensitive county-level awareness.

Content:

- County selector.
- Risk level.
- Explanation of risk scale.
- Safety guidance.
- Last updated timestamp.

### Resources

Purpose: provide support without requiring report submission.

Content:

- Safety planning.
- Rumor verification tips.
- Digital safety.
- Partner contact information where vetted.

### Settings

Purpose: user control and transparency.

Content:

- Language.
- Drafts.
- Privacy information.
- Delete local data.
- App version.

## Empty States

- No drafts: "You have no saved drafts."
- No network: "You can keep writing. This report will stay on this device until you submit it."
- No risk data: "Local guidance is temporarily unavailable. You can still report an incident."
- No resources loaded: show bundled offline resources.

## Error States

Errors should tell the user what happened, whether their report is safe, and what they can do next.

Examples:

- Submission failed: "Your report was not sent. It is saved on this device."
- Server unavailable: "AmaniPulse is temporarily unavailable. Try again later or use SMS/USSD if available."
- Location denied: "Location was not shared. You can choose a county manually."
- Draft encryption error: "For your safety, this draft cannot be saved. You can try submitting now or delete it."

## Trauma-Informed Copy Guidelines

- Use "You can" instead of "You must" where possible.
- Avoid graphic descriptions unless user-provided.
- Avoid political labels in UI examples.
- Avoid language that implies surveillance.
- Do not ask users to investigate further.
- Encourage moving to safety before reporting.

## Notification UX

Push notifications must be opt-in and non-sensitive.

Allowed examples:

- "AmaniPulse report status updated."
- "New safety guidance is available for your selected county."

Avoid:

- Incident category names.
- Report details.
- County risk escalation language that could cause panic.
- Anything that exposes the user's reporting activity on a lock screen.
