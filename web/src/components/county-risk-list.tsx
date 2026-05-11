import { countyRisks } from "@/lib/data";
import { trendLabel } from "@/lib/risk";
import { RiskBadge } from "@/components/risk-badge";

export function CountyRiskList() {
  return (
    <div className="county-list">
      {countyRisks.map((county) => (
        <article className="county-row" key={county.county}>
          <div>
            <strong>{county.county}</strong>
            <p>{county.region}</p>
          </div>
          <div className="score-bar" aria-label={`${county.county} risk score ${county.score}`}>
            <span style={{ width: `${county.score}%` }} />
          </div>
          <span className="trend-label">{trendLabel(county.trend)}</span>
          <RiskBadge level={county.level} />
        </article>
      ))}
    </div>
  );
}
