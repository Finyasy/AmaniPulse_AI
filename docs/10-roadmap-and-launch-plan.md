# Roadmap And Launch Plan

## Roadmap Goal

Deliver the AmaniPulse AI iPhone Citizen MVP in phases that protect users, validate community trust, and prepare the wider platform for election-period scale before the 2027 Kenya General Elections.

## Phase 1: Documentation And Validation

Objective: align product, safety, technical, and stakeholder expectations before implementation.

Key outcomes:

- Investor-ready product documentation.
- Citizen MVP scope confirmed.
- Safety and privacy principles defined.
- Initial UX flows documented.
- Partner assumptions identified.
- Pilot counties shortlisted.

Exit criteria:

- Stakeholders agree that the first app is citizen-facing only.
- Anonymity and location-sharing model is approved.
- English and Swahili launch requirement is accepted.
- Backend integration assumptions are clear.

## Phase 2: Prototype

Objective: build a clickable or lightweight native prototype for user validation.

Key outcomes:

- Onboarding prototype.
- Anonymous report flow prototype.
- Location consent prototype.
- Offline draft concept.
- Safety resources experience.
- English and Swahili copy review.

Exit criteria:

- Community users understand the reporting flow.
- Users understand saved versus submitted reports.
- Users understand that location is optional.
- Safety copy does not create false expectations.

## Phase 3: MVP Build

Objective: implement the Native SwiftUI Citizen MVP with staging backend integration.

Key outcomes:

- SwiftUI app shell.
- Anonymous reporting flow.
- Encrypted offline drafts.
- Manual and approximate location modes.
- App configuration API integration.
- Risk guidance display.
- Resource content caching.
- Accessibility and localization support.

Exit criteria:

- Core test suite passes.
- Privacy tests pass.
- Offline reporting flow is reliable.
- Staging APIs support report submission and risk guidance.
- Partner review approves field testing.

## Phase 4: Controlled Pilot

Objective: deploy to a limited trusted group before wider release.

Recommended pilot participants:

- Community peace volunteers.
- Civil society partners.
- Election observer support teams.
- Youth and faith-based peace networks.

Pilot goals:

- Validate trust and comprehension.
- Measure report completion.
- Test low-bandwidth behavior.
- Identify unsafe language or confusing flows.
- Validate moderation and escalation workflow.
- Confirm partner readiness to act on aggregated signals.

Exit criteria:

- No critical privacy or safety issues.
- Users can submit reports successfully in field conditions.
- Partner teams can interpret aggregated outputs responsibly.
- Support and incident response process is functional.

## Phase 5: Election Readiness

Objective: prepare for higher usage around major 2027 election milestones.

Key outcomes:

- Production backend hardening.
- Monitoring and alerting.
- Abuse and spam response.
- Model evaluation across language and region.
- Partner escalation playbooks.
- App Store release preparation.
- Public communication materials.

Exit criteria:

- Production release approved.
- Data governance process active.
- Critical-risk human review coverage defined.
- Partner channels ready.
- Public safety messaging reviewed.

## Phase 6: Post-Election Learning

Objective: preserve accountability, evaluate impact, and improve the platform for future peacebuilding contexts.

Key outcomes:

- Impact evaluation.
- Bias and model performance review.
- Community feedback synthesis.
- Data retention review.
- Partner retrospective.
- Roadmap for Android, SMS, USSD, WhatsApp, and dashboard expansion.

Exit criteria:

- Lessons documented.
- Sensitive data retention decisions completed.
- Product roadmap updated.
- Fundraising and scale strategy refined.

## Launch Workstreams

### Product

- Finalize Citizen MVP requirements.
- Maintain strict out-of-scope boundaries.
- Keep reporting flow short and safe.
- Validate all safety copy.

### Engineering

- Build Native SwiftUI app.
- Integrate staging APIs.
- Implement encrypted drafts.
- Add localization infrastructure.
- Add monitoring that excludes report content.

### AI And Data

- Define taxonomy and labels.
- Validate classification performance.
- Calibrate county risk scoring.
- Establish human review thresholds.
- Document model limitations.

### Safety And Governance

- Define data access policy.
- Define moderation roles.
- Define partner escalation.
- Prepare data request response process.
- Confirm privacy and security reviews.

### Partnerships

- Identify pilot counties.
- Vet local partner resources.
- Train pilot participants.
- Collect feedback safely.
- Align on intervention protocols.

## MVP Timeline Template

Suggested sequencing:

- Weeks 1-2: stakeholder validation and prototype.
- Weeks 3-6: MVP implementation.
- Weeks 7-8: localization, accessibility, and security hardening.
- Weeks 9-10: controlled pilot.
- Weeks 11-12: production readiness and launch decision.

Actual timing should adjust based on partner review, backend readiness, and safety findings.

## Launch Risks

- Users misunderstand anonymity.
- Users expect emergency response.
- Bad actors submit false reports.
- Risk guidance is perceived as partisan.
- Low-connectivity users cannot submit.
- Swahili translations miss local nuance.
- Partner teams lack capacity to act on signals.
- AI outputs are overtrusted.

Each risk should have a named owner before pilot launch.

## Success Criteria

- Citizen MVP launches without requiring accounts.
- Anonymous reporting is understandable and usable.
- Offline drafts work in field conditions.
- English and Swahili experiences are complete.
- Partner teams receive useful aggregated signals.
- Safety and privacy reviews pass before pilot.
- Community feedback indicates the app feels trustworthy.
