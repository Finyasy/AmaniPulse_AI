import Link from "next/link";
import {
  ArrowRight,
  Bell,
  ChevronRight,
  Languages,
  LockKeyhole,
  Map,
  ShieldAlert,
} from "lucide-react";
import {
  channels,
  countyRisks,
  publicPrinciples,
  responseTimeline,
  riskFeatures,
  siteMap,
} from "@/lib/data";
import { KenyaRiskMap } from "@/components/kenya-risk-map";
import { RiskBadge } from "@/components/risk-badge";
import { StatCard } from "@/components/stat-card";

export default function Home() {
  const leadingRisk = countyRisks[0];

  return (
    <main>
      <section className="hero-surface">
        <div className="hero-grid page-shell">
          <div className="hero-copy">
            <p className="eyebrow">Kenya 2027 election peace intelligence</p>
            <h1>AmaniPulse AI</h1>
            <p className="hero-lede">
              Anonymous community reporting, multilingual AI analysis, and
              county-level conflict risk scoring for prevention before
              escalation.
            </p>
          <div className="hero-actions" aria-label="Primary actions">
            <Link className="button button-primary" href="/report">
              <ShieldAlert aria-hidden="true" />
              Report safely
            </Link>
            <Link className="button button-secondary" href="/dashboard">
              <Map aria-hidden="true" />
              View dashboard
            </Link>
            <Link className="button button-secondary" href="/site-map">
              <ChevronRight aria-hidden="true" />
              Site map
            </Link>
          </div>
          </div>
          <div className="hero-visual" aria-label="Dashboard preview">
            <div className="dashboard-preview">
              <div className="preview-topbar">
                <span>Live peace posture</span>
                <RiskBadge level={leadingRisk.level} />
              </div>
              <KenyaRiskMap compact />
              <div className="preview-signal-row">
                <StatCard
                  label="Top hotspot"
                  value={leadingRisk.county}
                  detail={`${leadingRisk.score}/100 risk score`}
                />
                <StatCard
                  label="Signals"
                  value={`${leadingRisk.reports}`}
                  detail="Anonymous reports in 24h"
                />
              </div>
            </div>
          </div>
        </div>
      </section>

      <section className="section-band">
        <div className="page-shell section-heading">
          <p className="eyebrow">Platform map</p>
          <h2>One public website, one trusted partner surface.</h2>
          <p>
            The web experience is mapped around safe participation for citizens
            and explainable intelligence for NGOs, observers, and peace actors.
          </p>
          <Link className="text-link" href="/site-map">
            Open the full website map <ArrowRight aria-hidden="true" />
          </Link>
        </div>
        <div className="page-shell route-grid">
          {siteMap.map((route) => (
            <Link className="route-card" href={route.href} key={route.href}>
              <span>{route.label}</span>
              <p>{route.description}</p>
              <ChevronRight aria-hidden="true" />
            </Link>
          ))}
        </div>
      </section>

      <section className="section-band muted">
        <div className="page-shell split-layout">
          <div className="section-heading flush">
            <p className="eyebrow">Channels</p>
            <h2>Designed for low-bandwidth participation.</h2>
            <p>
              AmaniPulse should meet citizens where they already are: app,
              SMS, USSD, WhatsApp, and a lightweight web report form.
            </p>
          </div>
          <div className="channel-grid">
            {channels.map((channel) => {
              const Icon = channel.icon;
              return (
                <article className="info-card" key={channel.name}>
                  <div className="icon-tile">
                    <Icon aria-hidden="true" />
                  </div>
                  <div>
                    <div className="card-title-row">
                      <h3>{channel.name}</h3>
                      <span>{channel.status}</span>
                    </div>
                    <p>{channel.description}</p>
                  </div>
                </article>
              );
            })}
          </div>
        </div>
      </section>

      <section className="section-band">
        <div className="page-shell principles-grid">
          {publicPrinciples.map((principle) => {
            const Icon = principle.icon;
            return (
              <article className="principle" key={principle.title}>
                <Icon aria-hidden="true" />
                <h3>{principle.title}</h3>
                <p>{principle.body}</p>
              </article>
            );
          })}
        </div>
      </section>

      <section className="section-band muted">
        <div className="page-shell model-layout">
          <div className="section-heading flush">
            <p className="eyebrow">Risk model</p>
            <h2>Credit risk scoring logic, repurposed for peace.</h2>
            <p>
              The model watches for early warning signals and produces a clear
              conflict risk level that humans can verify and act on.
            </p>
          </div>
          <div className="feature-cloud" aria-label="Risk model features">
            {riskFeatures.map((feature) => (
              <span key={feature}>{feature}</span>
            ))}
          </div>
        </div>
      </section>

      <section className="section-band">
        <div className="page-shell timeline-layout">
          <div className="section-heading flush">
            <p className="eyebrow">Demo flow</p>
            <h2>From signal to prevention.</h2>
          </div>
          <div className="timeline">
            {responseTimeline.map((item) => {
              const Icon = item.icon;
              return (
                <article className="timeline-item" key={item.title}>
                  <span>{item.time}</span>
                  <Icon aria-hidden="true" />
                  <h3>{item.title}</h3>
                  <p>{item.body}</p>
                </article>
              );
            })}
          </div>
        </div>
      </section>

      <section className="cta-band">
        <div className="page-shell cta-layout">
          <div>
            <p className="eyebrow">Capstone-ready scope</p>
            <h2>Show the full AmaniPulse story without overbuilding admin tools.</h2>
          </div>
          <Link className="button button-primary" href="/dashboard/alerts">
            <Bell aria-hidden="true" />
            Review AI alerts
            <ArrowRight aria-hidden="true" />
          </Link>
        </div>
      </section>

      <footer className="site-footer">
        <div className="page-shell footer-grid">
          <span>AmaniPulse AI</span>
          <span>
            <LockKeyhole aria-hidden="true" /> Anonymous by default
          </span>
          <span>
            <Languages aria-hidden="true" /> English, Swahili, Sheng-ready
          </span>
        </div>
      </footer>
    </main>
  );
}
