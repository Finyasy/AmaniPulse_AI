import type { RiskLevel } from "@/lib/data";

export function riskClass(level: RiskLevel) {
  return `risk-${level.toLowerCase()}`;
}

export function trendLabel(trend: "up" | "down" | "flat") {
  if (trend === "up") return "Rising";
  if (trend === "down") return "Cooling";
  return "Stable";
}
