import { BellRing, HandHeart, ShieldCheck } from "lucide-react";
import { DashboardShell } from "@/components/dashboard-shell";
import { RiskBadge } from "@/components/risk-badge";
import { alerts } from "@/lib/data";

export default function AlertsPage() {
  return (
    <DashboardShell eyebrow="AI-assisted prevention" title="Alerts and interventions">
      <div className="alert-grid">
        {alerts.map((alert) => (
          <article className="dashboard-panel alert-panel" key={alert.title}>
            <div className="panel-heading">
              <div>
                <span>{alert.county} · {alert.window}</span>
                <h2>{alert.title}</h2>
              </div>
              <RiskBadge level={alert.level} />
            </div>
            <div className="alert-section">
              <BellRing aria-hidden="true" />
              <div>
                <strong>Why the model flagged this</strong>
                <p>{alert.rationale}</p>
              </div>
            </div>
            <div className="alert-section">
              <HandHeart aria-hidden="true" />
              <div>
                <strong>Recommended peace action</strong>
                <p>{alert.recommendation}</p>
              </div>
            </div>
          </article>
        ))}
      </div>

      <section className="dashboard-panel review-note">
        <ShieldCheck aria-hidden="true" />
        <div>
          <h2>Human review is required before action.</h2>
          <p>
            AmaniPulse AI should make risk explainable and timely, but sensitive
            election peace decisions need local context, language expertise, and
            trusted human judgment.
          </p>
        </div>
      </section>
    </DashboardShell>
  );
}
