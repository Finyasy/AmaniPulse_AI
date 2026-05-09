from enum import StrEnum


class IncidentCategory(StrEnum):
    violence_threat = "violence_threat"
    active_violence = "active_violence"
    voter_intimidation = "voter_intimidation"
    hate_speech_or_incitement = "hate_speech_or_incitement"
    misinformation_or_rumor = "misinformation_or_rumor"
    corruption_bribery_or_coercion = "corruption_bribery_or_coercion"
    authority_abuse = "authority_abuse"
    suspicious_mobilization = "suspicious_mobilization"
    other_election_safety_concern = "other_election_safety_concern"


class LocationMode(StrEnum):
    none = "none"
    manual_area = "manual_area"
    approximate_coordinates = "approximate_coordinates"


class ReportStatus(StrEnum):
    received = "received"
    under_review = "under_review"
    aggregated = "aggregated"
    closed = "closed"
    unable_to_process = "unable_to_process"


class RiskLevel(StrEnum):
    low = "low"
    moderate = "moderate"
    high = "high"
    critical = "critical"
