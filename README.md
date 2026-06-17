# AmaniPulse AI

AmaniPulse AI is an AI-powered PeaceTech platform designed to help prevent election-related violence and strengthen community accountability during the 2027 Kenya General Elections. The platform combines anonymous community reporting with predictive conflict early warning intelligence so communities, NGOs, election observers, and local peace actors can identify signs of unrest before escalation occurs.

This repository currently documents the **AmaniPulse AI iPhone Citizen MVP**, a Native SwiftUI application focused on safe anonymous reporting, multilingual civic access, low-bandwidth operation, and trusted peace information for community members.

## Why This Matters

Election periods can amplify misinformation, hate speech, intimidation, corruption, and localized political violence. Many warning signs appear early in community conversations, digital channels, and grassroots reports, but vulnerable people often lack a safe way to report what they see.

AmaniPulse AI turns scattered civic signals into actionable peace intelligence while preserving the dignity and safety of the people who report them.

## iPhone MVP Scope

The first iPhone application is citizen-facing only. It will help people:

- Submit anonymous incident reports.
- Report violence threats, voter intimidation, corruption, hate speech, and misinformation.
- Choose whether to share precise, approximate, or manually entered location context.
- Save reports offline and submit when connectivity returns.
- Access safety guidance and trusted community resources.
- Receive non-sensitive report status updates where appropriate.
- Use the app in English and Swahili first, with future support for additional local languages.

Responder dashboards, NGO triage consoles, SMS, USSD, WhatsApp, and predictive analytics services are treated as platform integrations rather than iPhone MVP features.

## Documentation Map

- [iPhone Frontend Implementation](ios/AmaniPulseCitizen/README.md)
- [Backend Implementation](backend/README.md)
- [Product Brief](docs/01-product-brief.md)
- [iPhone App PRD](docs/02-iphone-app-prd.md)
- [User Experience](docs/03-user-experience.md)
- [Technical Architecture](docs/04-technical-architecture.md)
- [Data and API Contracts](docs/05-data-and-api-contracts.md)
- [AI and Risk Scoring](docs/06-ai-and-risk-scoring.md)
- [Safety, Privacy, and Security](docs/07-safety-privacy-security.md)
- [Accessibility, Localization, and Low Bandwidth](docs/08-accessibility-localization-low-bandwidth.md)
- [Testing and Quality](docs/09-testing-and-quality.md)
- [Roadmap and Launch Plan](docs/10-roadmap-and-launch-plan.md)
- [Andela x Open Accelerator Runbook](docs/11-andela-open-accelerator-runbook.md)

## Product Principles

- **Safety before data collection:** the app should never pressure a vulnerable person to disclose more than they safely can.
- **Anonymity by default:** no account, name, phone number, email, or device identity should be required for citizen reporting.
- **Low-bandwidth by design:** the core reporting path must remain usable under unreliable network conditions.
- **Local language access:** English and Swahili are launch requirements, not future polish.
- **Human-centered AI:** AI should support early warning and triage, not replace human judgment in sensitive peacebuilding decisions.
- **Prevention over reaction:** the product should help communities intervene before harm escalates.

## Target Stakeholders

- Community members and vulnerable citizens.
- Youth peacebuilders and civic volunteers.
- NGOs and civil society organizations.
- Election observers and monitoring coalitions.
- Local leaders and trusted peace actors.
- Researchers and funders evaluating responsible AI for peacebuilding.

## Repository Status

This repository is currently documentation-first with an initial FastAPI backend scaffold and the first SwiftUI package for the iPhone Citizen frontend. No dashboard code is included yet.

Recommended next step after this documentation phase:

1. Validate the Citizen MVP with peacebuilding stakeholders and community representatives.
2. Continue hardening the FastAPI backend with PostgreSQL/PostGIS and Redis/Celery.
3. Wrap the SwiftUI package in an iOS app target and continue the anonymous reporting flow.
4. Implement encrypted offline draft storage and backend API clients.
5. Conduct privacy, safety, and localization review before pilot deployment.

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE).
