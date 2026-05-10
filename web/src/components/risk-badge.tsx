import type { RiskLevel } from "@/lib/data";
import { riskClass } from "@/lib/risk";

export function RiskBadge({ level }: { level: RiskLevel }) {
  return <span className={`risk-badge ${riskClass(level)}`}>{level}</span>;
}
