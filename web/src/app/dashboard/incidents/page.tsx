import { DashboardShell } from "@/components/dashboard-shell";
import { IncidentsTable } from "@/components/incidents-table";

export default function IncidentsPage() {
  return (
    <DashboardShell eyebrow="Anonymous signal review" title="Incident stream">
      <section className="dashboard-panel">
        <div className="panel-heading">
          <div>
            <span>Latest reports</span>
            <h2>Anonymized reports for triage</h2>
          </div>
        </div>
        <IncidentsTable />
      </section>
    </DashboardShell>
  );
}
