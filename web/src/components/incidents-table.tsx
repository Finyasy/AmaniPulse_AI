import { incidents } from "@/lib/data";
import { RiskBadge } from "@/components/risk-badge";

export function IncidentsTable({ limit }: { limit?: number }) {
  const visibleIncidents = limit ? incidents.slice(0, limit) : incidents;

  return (
    <div className="table-panel">
      <div className="table-header">
        <span>Incident</span>
        <span>County</span>
        <span>Category</span>
        <span>Severity</span>
      </div>
      {visibleIncidents.map((incident) => (
        <article className="incident-row" key={incident.id}>
          <div>
            <strong>{incident.id}</strong>
            <p>{incident.summary}</p>
            <small>
              {incident.area} · {incident.language} · {incident.received}
            </small>
          </div>
          <span>{incident.county}</span>
          <span>{incident.category}</span>
          <RiskBadge level={incident.severity} />
        </article>
      ))}
    </div>
  );
}
