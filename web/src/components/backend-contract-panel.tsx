import { PlugZap, ShieldCheck, Workflow } from "lucide-react";

const contractItems = [
  {
    title: "Citizen report intake",
    body: "The web form now prepares ReportCreate-compatible payloads with category, location mode, language, and consent fields.",
    icon: ShieldCheck,
  },
  {
    title: "Risk intelligence",
    body: "Dashboard risk cards are shaped around CountyRiskResponse so FastAPI county endpoints can replace mocks.",
    icon: PlugZap,
  },
  {
    title: "Partner review",
    body: "The review queue mirrors backend review summaries, AI labels, and audit events without exposing admin controls.",
    icon: Workflow,
  },
];

export function BackendContractPanel() {
  return (
    <section className="dashboard-panel contract-panel">
      <div className="panel-heading">
        <div>
          <span>Backend alignment</span>
          <h2>Ready for FastAPI handoff</h2>
        </div>
      </div>
      <div className="contract-grid">
        {contractItems.map((item) => {
          const Icon = item.icon;
          return (
            <article key={item.title}>
              <Icon aria-hidden="true" />
              <h3>{item.title}</h3>
              <p>{item.body}</p>
            </article>
          );
        })}
      </div>
    </section>
  );
}
