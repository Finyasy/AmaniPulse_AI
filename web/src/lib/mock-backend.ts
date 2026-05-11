import type {
  CountyRiskResponse,
  ReportCreatePayload,
  ReportReceipt,
  ReviewEventItem,
  ReviewReportDetail,
  ReviewReportSummary,
} from "@/lib/contracts";

const now = "2026-05-10T09:00:00.000Z";

export const mockCountyRiskResponses: CountyRiskResponse[] = [
  {
    county_code: "047",
    county_name: "Nairobi",
    risk_level: "high",
    score: 84,
    updated_at: now,
    summary: "Report volume and intimidation terms are rising around two urban rally corridors.",
    guidance: [
      "Verify with trusted community mediators.",
      "Increase observer coverage around transit points.",
      "Publish rumor-correction messaging in English, Swahili, and Sheng.",
    ],
  },
  {
    county_code: "042",
    county_name: "Kisumu",
    risk_level: "high",
    score: 76,
    updated_at: now,
    summary: "Protest chatter and localized fear sentiment are above the guarded baseline.",
    guidance: [
      "Coordinate with local peace committees.",
      "Monitor transport disruption signals.",
      "Prepare de-escalation messaging before planned gatherings.",
    ],
  },
  {
    county_code: "027",
    county_name: "Uasin Gishu",
    risk_level: "moderate",
    score: 69,
    updated_at: now,
    summary: "Coded incitement and mobilization signals need human language-context review.",
    guidance: [
      "Route flagged phrases to a trained reviewer.",
      "Avoid automated action until local context is confirmed.",
      "Ask observers to validate youth mobilization reports.",
    ],
  },
  {
    county_code: "001",
    county_name: "Mombasa",
    risk_level: "moderate",
    score: 58,
    updated_at: now,
    summary: "Rumor correction activity is improving the risk trend, but signal density remains guarded.",
    guidance: ["Continue rumor correction.", "Maintain light observer coverage."],
  },
];

export const mockReviewQueue: ReviewReportDetail[] = [
  {
    report_reference: "AP-2714",
    category: "suspicious_mobilization",
    status: "under_review",
    incident_time: "2026-05-10T08:26:00.000Z",
    received_at: "2026-05-10T08:31:00.000Z",
    updated_at: "2026-05-10T08:39:00.000Z",
    county: "Nairobi",
    area_label: "Mathare",
    language: "sheng",
    severity_score: 88,
    urgency: "immediate",
    needs_human_review: true,
    description: "Multiple anonymous reports mention youth groups gathering after a campaign rally.",
    ai_labels: {
      threat_terms: 7,
      location_confidence: "medium",
      multilingual_review_needed: true,
      duplicate_cluster_size: 4,
    },
  },
  {
    report_reference: "AP-2713",
    category: "corruption_bribery_or_coercion",
    status: "under_review",
    incident_time: "2026-05-10T08:12:00.000Z",
    received_at: "2026-05-10T08:21:00.000Z",
    updated_at: "2026-05-10T08:32:00.000Z",
    county: "Nakuru",
    area_label: "Naivasha",
    language: "sw",
    severity_score: 71,
    urgency: "today",
    needs_human_review: true,
    description: "Residents report cash distribution near a transit point with rising crowd tension.",
    ai_labels: {
      coercion_signal: "probable",
      crowd_tension: "elevated",
      duplicate_cluster_size: 2,
    },
  },
  {
    report_reference: "AP-2712",
    category: "voter_intimidation",
    status: "received",
    incident_time: "2026-05-10T07:52:00.000Z",
    received_at: "2026-05-10T08:03:00.000Z",
    updated_at: "2026-05-10T08:04:00.000Z",
    county: "Kisumu",
    area_label: "Kondele",
    language: "en",
    severity_score: 66,
    urgency: "today",
    needs_human_review: true,
    description: "Observer signal notes protest planning and fear of confrontation with police.",
    ai_labels: {
      protest_escalation: "possible",
      authority_contact: true,
      duplicate_cluster_size: 1,
    },
  },
];

export const mockReviewEvents: ReviewEventItem[] = [
  {
    report_reference: "AP-2714",
    reviewer_id: "peace-desk",
    previous_status: "received",
    new_status: "under_review",
    note: "Queued for human context review because the report uses Sheng and references mobilization.",
    created_at: "2026-05-10T08:39:00.000Z",
  },
  {
    report_reference: "AP-2713",
    reviewer_id: "triage-lead",
    previous_status: "received",
    new_status: "under_review",
    note: "Escalated for partner verification near transport corridor.",
    created_at: "2026-05-10T08:32:00.000Z",
  },
  {
    report_reference: "AP-2710",
    reviewer_id: "rumor-desk",
    previous_status: "under_review",
    new_status: "aggregated",
    note: "Merged into county rumor trend after two partner confirmations.",
    created_at: "2026-05-10T07:45:00.000Z",
  },
];

export function createMockReceipt(payload: ReportCreatePayload): ReportReceipt {
  const suffix = payload.client_report_id.slice(-6).toUpperCase();

  return {
    report_reference: `WEB-${suffix}`,
    status: "received",
    received_at: new Date().toISOString(),
    message: "Report received. Keep your reference somewhere safe if you want to check status later.",
  };
}

export function reviewSummaries(): ReviewReportSummary[] {
  return mockReviewQueue.map(({ description: _description, ai_labels: _aiLabels, ...summary }) => summary);
}
