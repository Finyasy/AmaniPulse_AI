import Foundation

public enum IncidentCategory: String, CaseIterable, Codable, Identifiable, Sendable {
    case violenceThreat = "violence_threat"
    case activeViolence = "active_violence"
    case voterIntimidation = "voter_intimidation"
    case hateSpeechOrIncitement = "hate_speech_or_incitement"
    case misinformationOrRumor = "misinformation_or_rumor"
    case corruptionBriberyOrCoercion = "corruption_bribery_or_coercion"
    case authorityAbuse = "authority_abuse"
    case suspiciousMobilization = "suspicious_mobilization"
    case otherElectionSafetyConcern = "other_election_safety_concern"

    public var id: String { rawValue }
}
