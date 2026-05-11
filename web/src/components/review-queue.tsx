import { AlertCircle, ClipboardCheck, History, Languages } from "lucide-react";
import { categoryLabel, statusLabel } from "@/lib/contracts";
import type { ReviewEventItem, ReviewReportDetail } from "@/lib/contracts";

function formatDateTime(value: string) {
  return new Intl.DateTimeFormat("en-KE", {
    dateStyle: "medium",
    timeStyle: "short",
    timeZone: "Africa/Nairobi",
  }).format(new Date(value));
}

export function ReviewQueue({
  reports,
  events,
}: {
  reports: ReviewReportDetail[];
  events: ReviewEventItem[];
}) {
  return (
    <div className="review-layout">
      <section className="dashboard-panel">
        <div className="panel-heading">
          <div>
            <span>Human review queue</span>
            <h2>Reports needing partner context</h2>
          </div>
        </div>
        <div className="review-card-list">
          {reports.map((report) => (
            <article className="review-card" key={report.report_reference}>
              <div className="review-card-top">
                <div>
                  <strong>{report.report_reference}</strong>
                  <p>{categoryLabel(report.category)}</p>
                </div>
                <span className="status-pill">{statusLabel(report.status)}</span>
              </div>
              <p className="review-description">{report.description}</p>
              <div className="review-meta-grid">
                <span>
                  <AlertCircle aria-hidden="true" />
                  Score {report.severity_score ?? "n/a"}
                </span>
                <span>
                  <Languages aria-hidden="true" />
                  {report.language.toUpperCase()}
                </span>
                <span>
                  <ClipboardCheck aria-hidden="true" />
                  {report.urgency ?? "review"}
                </span>
              </div>
              <dl className="ai-labels">
                {Object.entries(report.ai_labels).map(([key, value]) => (
                  <div key={key}>
                    <dt>{key.replaceAll("_", " ")}</dt>
                    <dd>{String(value)}</dd>
                  </div>
                ))}
              </dl>
            </article>
          ))}
        </div>
      </section>

      <section className="dashboard-panel">
        <div className="panel-heading">
          <div>
            <span>Audit trail</span>
            <h2>Review events</h2>
          </div>
        </div>
        <div className="event-list">
          {events.map((event) => (
            <article className="event-row" key={`${event.report_reference}-${event.created_at}`}>
              <History aria-hidden="true" />
              <div>
                <strong>
                  {event.report_reference} · {statusLabel(event.new_status)}
                </strong>
                <p>{event.note}</p>
                <small>
                  {event.reviewer_id} · {formatDateTime(event.created_at)}
                </small>
              </div>
            </article>
          ))}
        </div>
      </section>
    </div>
  );
}
