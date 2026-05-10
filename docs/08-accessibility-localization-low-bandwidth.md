# Accessibility, Localization, And Low Bandwidth

## Goal

AmaniPulse AI must be usable by people with different languages, abilities, devices, literacy levels, and network conditions. These are core requirements for the Citizen MVP, not optional enhancements.

## Launch Languages

MVP languages:

- English.
- Swahili.

The app should be structured to support future local languages without redesigning the reporting flow.

## Localization Requirements

- All user-facing strings must be localizable.
- Incident categories must have localized names and descriptions.
- Safety guidance must be reviewed by fluent speakers.
- Avoid idioms that do not translate well.
- Support remote updates to resource content.
- Use culturally neutral examples.
- Avoid politically loaded terms unless required for clarity.

## Language Selection

The app should:

- Detect the iOS preferred language where possible.
- Ask users to confirm language on first launch.
- Allow language changes in settings.
- Avoid forcing the user through onboarding again after language changes.
- Cache selected language locally.

## Writing Style

Copy should be:

- Short.
- Calm.
- Direct.
- Non-technical.
- Non-partisan.
- Easy to translate.
- Safe for stressed users.

Example:

```text
Move to safety first. You can report when it is safe.
```

Avoid:

```text
Submit all evidence immediately for urgent escalation.
```

## Accessibility Requirements

### VoiceOver

- Every interactive element has a meaningful accessibility label.
- Category cards describe both title and meaning.
- Risk levels include text, not color alone.
- Form errors are announced clearly.
- Confirmation states are readable without visual context.

### Dynamic Type

- Support larger text sizes.
- Avoid fixed-height text containers.
- Ensure buttons remain usable at accessibility sizes.
- Test report flow with large text.

### Color And Contrast

- Meet WCAG AA contrast guidance.
- Do not communicate risk by color alone.
- Use icon and text labels for risk levels.
- Avoid alarming red-heavy screens except where truly necessary.

### Motor Accessibility

- Use large tap targets.
- Avoid time-limited flows.
- Support saving drafts.
- Avoid complex gestures.
- Keep primary actions reachable.

### Cognitive Accessibility

- Break reporting into simple steps.
- Use progress indicators.
- Avoid dense paragraphs.
- Confirm before submission.
- Provide examples without leading users.

## Low-Bandwidth Requirements

The app should:

- Keep report payloads small.
- Avoid loading heavy images or maps in the core report flow.
- Cache configuration and resources.
- Bundle essential safety resources.
- Allow offline drafts.
- Retry failed submissions safely.
- Show network state in plain language.
- Avoid auto-uploading media in MVP.

## Offline Behavior

When offline:

- The user can start and save a report.
- The app clearly says the report has not been submitted.
- The user can edit or delete the draft.
- The app can display bundled resources.
- The app can show cached risk guidance with timestamp.
- The app should not imply that a report has reached AmaniPulse.

When connectivity returns:

- The user can manually submit saved drafts.
- Automatic retry should be transparent and configurable.
- Duplicate submissions should be prevented with `client_report_id`.

## Data Usage Strategy

- Prefer JSON configuration over heavy remote assets.
- Use pagination or small resource bundles if needed.
- Compress API responses where practical.
- Avoid always-on polling.
- Use push notifications only for generic updates.
- Cache county risk guidance for reasonable intervals.

## Device Support

The MVP should target currently supported iOS versions that allow modern SwiftUI, privacy controls, and security updates. Older unsupported iOS versions should not be targeted if doing so weakens safety or maintainability.

## Field Testing Scenarios

Test the app under:

- 2G-like network speed.
- Intermittent connectivity.
- Airplane mode.
- Low battery mode.
- Small screen devices.
- Large Dynamic Type.
- VoiceOver enabled.
- English and Swahili.
- First launch without network.

## Acceptance Criteria

- A user can submit the MVP report flow in English and Swahili.
- A user can use the report flow with VoiceOver.
- A user can use the app with large text enabled.
- A user can save a report offline and understand it is not submitted yet.
- A user can access safety resources without network.
- Risk levels remain understandable without color.
