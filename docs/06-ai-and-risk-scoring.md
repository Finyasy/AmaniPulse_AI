# AI And Risk Scoring

## Purpose

AmaniPulse AI uses AI to help detect early warning signals, classify reports, and estimate regional conflict risk. AI should support prevention and prioritization, not replace human judgment or community accountability.

The iPhone app is not expected to run the full AI pipeline locally. It submits anonymous reports and displays safe, aggregated guidance returned by backend services.

## AI Capabilities

Backend AI services may support:

- NLP sentiment analysis.
- Hate speech and incitement detection.
- Misinformation and rumor signal detection.
- Report category classification.
- Duplicate and cluster detection.
- Time-series anomaly detection.
- Geo-based conflict risk scoring.
- Human review prioritization.

## Input Signals

Potential platform signals include:

- Anonymous citizen reports from the iPhone app.
- SMS, USSD, and WhatsApp reports.
- Public online discourse where legally and ethically collected.
- Historical incident patterns.
- County-level report frequency.
- Partner-verified field observations.
- Public election timeline events.

Sensitive or private sources must not be used without explicit legal basis, consent, and ethical review.

## Report Classification

Each report may be classified by:

- Incident category.
- Severity.
- Urgency.
- Location confidence.
- Language.
- Harm type.
- Potential target group, only when necessary and handled carefully.
- Need for human review.

Classification confidence should be stored and reviewed. Low-confidence or high-severity reports should be escalated to human reviewers rather than automatically acted on.

## Hate Speech And Escalation Detection

The system should identify patterns such as:

- Dehumanizing language.
- Calls for violence.
- Threats against political, ethnic, religious, or regional groups.
- Mobilization language.
- Revenge or retaliation framing.
- Repeated rumor narratives.

Models must be localized for Kenyan and regional language contexts. Literal keyword matching is not sufficient because language can be coded, sarcastic, translated, or context-specific.

## Misinformation Detection

The system may flag:

- Unverified claims about polling places.
- False claims about voter eligibility.
- Fabricated violence reports intended to trigger panic.
- Manipulated media references.
- Coordinated rumor spread across regions.

The product should avoid labeling claims publicly unless verified. In citizen-facing UX, misinformation handling should emphasize "verify before sharing" rather than accusing users.

## Time-Series Anomaly Detection

Anomaly detection should compare current signals against expected baselines:

- Report volume by county.
- Category spikes.
- Language or keyword clusters.
- Sudden geographic concentration.
- Repeat mentions of locations or actors.
- Increased severity within a short window.

Anomaly detection should account for election calendar events, rallies, court rulings, registration deadlines, and known high-attention periods.

## County Risk Score

Risk score should combine multiple factors:

- Recent report volume.
- Report severity.
- Category mix.
- Location concentration.
- Duplicate cluster strength.
- Hate speech or escalation indicators.
- Historical risk context.
- Partner verification signals.
- Recency and trend direction.

Recommended public scale:

- **Low:** no unusual risk signals detected.
- **Moderate:** elevated signals that deserve awareness.
- **High:** strong signals that may require partner attention.
- **Critical:** urgent escalation indicators requiring immediate human review and partner coordination.

The citizen app should display only safe public guidance, not raw scoring details.

## Human Review Boundaries

Human review is required for:

- Critical risk escalation.
- Reports alleging imminent violence.
- Reports involving named individuals or groups.
- Ambiguous hate speech classification.
- Potential misinformation claims with public safety implications.
- Requests from trusted partner organizations.

AI should never automatically publish accusations, identify alleged perpetrators, or trigger coercive action without review.

## Model Limitations

Known risks:

- Bias against dialects or minority language patterns.
- False positives around reclaimed or quoted language.
- False negatives for coded threats.
- Overweighting highly connected urban reports.
- Underrepresenting communities with limited phone access.
- Coordinated spam or manipulation.
- Misinterpreting jokes, satire, or political slogans.

These limitations should be documented for partners and reflected in model evaluation.

## Responsible AI Requirements

- Keep human oversight for high-impact decisions.
- Track model confidence and uncertainty.
- Evaluate performance across languages and regions.
- Avoid public release of raw sensitive data.
- Minimize personally identifying information in training data.
- Maintain audit logs for backend moderation actions.
- Provide a process for correcting taxonomy or model errors.
- Do not use AI outputs as sole evidence for punitive action.

## iPhone App AI Responsibilities

The app should:

- Collect structured reports that improve classification quality.
- Warn users not to include personal details.
- Display only safe, aggregated risk guidance.
- Avoid making claims that AI predictions are certain.
- Avoid exposing model labels that could inflame tensions.
- Support local language input.

The app should not:

- Run high-stakes local predictions on device for MVP.
- Show raw AI confidence scores to citizens.
- Display alleged culprit names.
- Present county risk levels as confirmed forecasts.
- Use report text for unrelated AI training without consent.

## Evaluation Metrics

- Category classification precision and recall.
- Hate speech detection false positive and false negative rates.
- Misinformation flag review accuracy.
- Critical incident detection latency.
- County-level risk calibration.
- Human reviewer agreement.
- Language parity across English, Swahili, and future local languages.
- Abuse and spam detection performance.
