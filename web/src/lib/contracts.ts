export type ApiIncidentCategory =
  | "violence_threat"
  | "active_violence"
  | "voter_intimidation"
  | "hate_speech_or_incitement"
  | "misinformation_or_rumor"
  | "corruption_bribery_or_coercion"
  | "authority_abuse"
  | "suspicious_mobilization"
  | "other_election_safety_concern";

export type ApiLocationMode = "none" | "manual_area" | "approximate_coordinates";
export type ApiReportStatus =
  | "received"
  | "under_review"
  | "aggregated"
  | "closed"
  | "unable_to_process";
export type ApiRiskLevel = "low" | "moderate" | "high" | "critical";
export type ApiLanguage = "en" | "sw";

export type ReportCreatePayload = {
  client_report_id: string;
  category: ApiIncidentCategory;
  description: string;
  incident_time: string;
  location: {
    mode: ApiLocationMode;
    country?: "KE";
    county?: string;
    area_label?: string;
    latitude_rounded?: number;
    longitude_rounded?: number;
    precision_km?: number;
  };
  language: ApiLanguage;
  source: "ios_citizen_app";
  app_version: string;
  consents: {
    anonymous_submission: boolean;
    risk_analysis: boolean;
  };
};

export type ReportReceipt = {
  report_reference: string;
  status: ApiReportStatus;
  received_at: string;
  message: string;
};

export type ReviewReportSummary = {
  report_reference: string;
  category: ApiIncidentCategory;
  status: ApiReportStatus;
  incident_time: string;
  received_at: string;
  updated_at: string;
  county: string | null;
  area_label: string | null;
  language: string;
  severity_score: number | null;
  urgency: string | null;
  needs_human_review: boolean | null;
};

export type ReviewReportDetail = ReviewReportSummary & {
  description: string;
  ai_labels: Record<string, string | number | boolean>;
};

export type ReviewEventItem = {
  report_reference: string;
  reviewer_id: string;
  previous_status: ApiReportStatus;
  new_status: ApiReportStatus;
  note: string;
  created_at: string;
};

export type CountyRiskResponse = {
  county_code: string;
  county_name: string;
  risk_level: ApiRiskLevel;
  score: number;
  updated_at: string;
  summary: string;
  guidance: string[];
};

export type IncidentTaxonomyItem = {
  id: ApiIncidentCategory;
  name: string;
  description: string;
  safety_guidance: string;
};

export type ResourceItem = {
  id: string;
  title: string;
  body: string;
  category: string;
  updated_at: string;
};

export const incidentCategoryOptions: Array<{
  value: ApiIncidentCategory;
  label: string;
}> = [
  { value: "violence_threat", label: "Violence threat" },
  { value: "active_violence", label: "Active violence" },
  { value: "voter_intimidation", label: "Voter intimidation" },
  { value: "hate_speech_or_incitement", label: "Hate speech or incitement" },
  { value: "misinformation_or_rumor", label: "Misinformation or rumor" },
  { value: "corruption_bribery_or_coercion", label: "Bribery, coercion, or corruption" },
  { value: "authority_abuse", label: "Authority abuse" },
  { value: "suspicious_mobilization", label: "Suspicious mobilization" },
  { value: "other_election_safety_concern", label: "Other election safety concern" },
];

export function categoryLabel(category: ApiIncidentCategory) {
  return incidentCategoryOptions.find((option) => option.value === category)?.label ?? category;
}

export function statusLabel(status: ApiReportStatus) {
  return status.replaceAll("_", " ");
}
