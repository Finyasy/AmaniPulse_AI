# AmaniPulse AI Web Platform

This web app turns the AmaniPulse AI concept into a capstone-ready product surface: a public low-bandwidth website, an anonymous web reporting flow, and a protected-style partner dashboard using demo election peace risk data.

## Why This Website Exists

The existing product docs define the Citizen MVP as an iPhone-first reporting app and explicitly keep responder/admin functionality out of that MVP. This web app is therefore framed differently: it is not a case-management admin panel. It is a demo-ready Election Peace Intelligence website that helps explain the broader AmaniPulse AI platform and show how trusted partners could act on anonymized risk signals.

## Website Map

- `/` - Public product overview with the platform promise, channels, risk model, and dashboard preview.
- `/site-map` - Frontend route map and implementation phases for reviewers.
- `/report` - Anonymous low-bandwidth web report form for citizens who cannot use the iPhone app, SMS, USSD, or WhatsApp.
- `/resources` - Safety guidance, trusted support categories, and low-data civic participation tips.
- `/dashboard` - Partner intelligence overview with national risk posture, county signals, and operational priorities.
- `/dashboard/map` - Kenya risk heatmap view with county-level synthetic scores.
- `/dashboard/incidents` - Anonymized incident stream for triage and pattern review.
- `/dashboard/alerts` - AI-generated escalation alerts and recommended peace interventions.

## Product Boundary

This build intentionally avoids:

- Citizen accounts.
- Public raw report feeds.
- Law enforcement dispatch.
- Full case management.
- Editing backend content or user permissions.

Those are future platform capabilities, not the first web demo.

## Technical Direction

- Framework: Next.js App Router with TypeScript.
- Styling: Plain CSS in `src/app/globals.css` to keep the prototype easy to inspect.
- Data: Mock election-risk data in `src/lib/data.ts`, ready to be swapped for FastAPI endpoints later.
- UI posture: Low-bandwidth, accessible, calm, and operational rather than a glossy marketing page.

## Demo Story

The intended capstone flow is:

1. A citizen submits an anonymous report through `/report`.
2. Reports and multilingual risk signals feed the AI risk engine.
3. County risk scores update in the partner dashboard.
4. Trusted partners review alerts and recommended interventions.
5. The system supports prevention before escalation.
