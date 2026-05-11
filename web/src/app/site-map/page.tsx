import Link from "next/link";
import { ArrowRight, Compass, FileText, GitBranch } from "lucide-react";
import { siteMap } from "@/lib/data";

const implementationPhases = [
  {
    title: "Public website",
    body: "Explain the platform, safety promise, reporting channels, and capstone demo story.",
  },
  {
    title: "Citizen reporting",
    body: "Provide a low-bandwidth anonymous web form that mirrors the future app, SMS, and USSD intake paths.",
  },
  {
    title: "Partner intelligence",
    body: "Show risk scores, a Kenya hotspot map, anonymized incidents, and AI intervention alerts.",
  },
  {
    title: "Backend integration",
    body: "Replace mock data with FastAPI endpoints for reports, taxonomy, risk scores, and alert review.",
  },
];

export default function SiteMapPage() {
  return (
    <main>
      <section className="page-hero">
        <div className="page-shell narrow">
          <p className="eyebrow">Website map</p>
          <h1>The AmaniPulse AI frontend is organized around action.</h1>
          <p>
            Citizens get safe participation routes. Trusted partners get the
            intelligence surface needed to prevent escalation.
          </p>
        </div>
      </section>

      <section className="section-band">
        <div className="page-shell sitemap-layout">
          <div className="sitemap-panel">
            <div className="sitemap-panel-heading">
              <Compass aria-hidden="true" />
              <h2>Route structure</h2>
            </div>
            <div className="sitemap-tree">
              {siteMap.map((route) => (
                <Link href={route.href} key={route.href}>
                  <span>{route.href}</span>
                  <strong>{route.label}</strong>
                  <p>{route.description}</p>
                  <ArrowRight aria-hidden="true" />
                </Link>
              ))}
            </div>
          </div>

          <div className="sitemap-panel">
            <div className="sitemap-panel-heading">
              <GitBranch aria-hidden="true" />
              <h2>Implementation phases</h2>
            </div>
            <div className="phase-list">
              {implementationPhases.map((phase, index) => (
                <article key={phase.title}>
                  <span>{String(index + 1).padStart(2, "0")}</span>
                  <div>
                    <h3>{phase.title}</h3>
                    <p>{phase.body}</p>
                  </div>
                </article>
              ))}
            </div>
          </div>
        </div>
      </section>

      <section className="section-band muted">
        <div className="page-shell doc-callout">
          <FileText aria-hidden="true" />
          <div>
            <h2>Implementation notes live in the repo.</h2>
            <p>
              The Markdown explainer documents the website purpose, product
              boundary, route map, and capstone demo story.
            </p>
          </div>
        </div>
      </section>
    </main>
  );
}
