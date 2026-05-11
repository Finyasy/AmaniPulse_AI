import { CountyRiskList } from "@/components/county-risk-list";
import { DashboardShell } from "@/components/dashboard-shell";
import { KenyaRiskMap } from "@/components/kenya-risk-map";
import { RiskBadge } from "@/components/risk-badge";
import { countyRisks } from "@/lib/data";

export default function DashboardMapPage() {
  return (
    <DashboardShell eyebrow="Geographic early warning" title="County risk map">
      <section className="dashboard-panel map-panel wide">
        <div className="panel-heading">
          <div>
            <span>Demo heatmap</span>
            <h2>Kenya election risk posture</h2>
          </div>
          <div className="map-legend" aria-label="Risk legend">
            <RiskBadge level="LOW" />
            <RiskBadge level="GUARDED" />
            <RiskBadge level="ELEVATED" />
            <RiskBadge level="HIGH" />
          </div>
        </div>
        <KenyaRiskMap />
      </section>

      <section className="dashboard-panel">
        <div className="panel-heading">
          <div>
            <span>County list</span>
            <h2>Risk score and signal drivers</h2>
          </div>
        </div>
        <CountyRiskList />
      </section>

      <div className="driver-grid">
        {countyRisks.slice(0, 4).map((county) => (
          <article className="dashboard-panel driver-panel" key={county.county}>
            <div className="panel-heading">
              <div>
                <span>{county.region}</span>
                <h2>{county.county}</h2>
              </div>
              <RiskBadge level={county.level} />
            </div>
            <ul>
              {county.drivers.map((driver) => (
                <li key={driver}>{driver}</li>
              ))}
            </ul>
          </article>
        ))}
      </div>
    </DashboardShell>
  );
}
