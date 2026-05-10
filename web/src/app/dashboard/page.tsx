import Link from "next/link";
import { ArrowRight } from "lucide-react";
import { CountyRiskList } from "@/components/county-risk-list";
import { DashboardShell } from "@/components/dashboard-shell";
import { IncidentsTable } from "@/components/incidents-table";
import { KenyaRiskMap } from "@/components/kenya-risk-map";
import { StatCard } from "@/components/stat-card";
import { dashboardStats } from "@/lib/data";

export default function DashboardPage() {
  return (
    <DashboardShell
      eyebrow="Election peace intelligence"
      title="National risk overview"
    >
      <div className="stat-grid">
        {dashboardStats.map((stat) => (
          <StatCard
            detail={stat.detail}
            icon={stat.icon}
            key={stat.label}
            label={stat.label}
            value={stat.value}
          />
        ))}
      </div>

      <div className="dashboard-grid">
        <section className="dashboard-panel map-panel">
          <div className="panel-heading">
            <div>
              <span>County risk map</span>
              <h2>Kenya hotspot posture</h2>
            </div>
            <Link href="/dashboard/map">
              Open map <ArrowRight aria-hidden="true" />
            </Link>
          </div>
          <KenyaRiskMap />
        </section>

        <section className="dashboard-panel">
          <div className="panel-heading">
            <div>
              <span>Risk ranking</span>
              <h2>Counties to watch</h2>
            </div>
          </div>
          <CountyRiskList />
        </section>
      </div>

      <section className="dashboard-panel">
        <div className="panel-heading">
          <div>
            <span>Anonymized reports</span>
            <h2>Latest incident stream</h2>
          </div>
          <Link href="/dashboard/incidents">
            View all <ArrowRight aria-hidden="true" />
          </Link>
        </div>
        <IncidentsTable limit={3} />
      </section>
    </DashboardShell>
  );
}
