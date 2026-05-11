import Foundation

public enum ReportStatus: String, Codable, Sendable {
    case draft
    case waitingForNetwork = "waiting_for_network"
    case submitted
    case received
    case underReview = "under_review"
    case aggregated
    case closed
    case unableToProcess = "unable_to_process"
}

public struct ReportDraft: Codable, Identifiable, Equatable, Sendable {
    public var id: UUID
    public var category: IncidentCategory?
    public var description: String
    public var incidentTime: Date
    public var location: LocationChoice
    public var language: AppLanguage
    public var acceptedSafetyReminder: Bool
    public var status: ReportStatus
    public var reportReference: String?

    public init(
        id: UUID = UUID(),
        category: IncidentCategory? = nil,
        description: String = "",
        incidentTime: Date = .now,
        location: LocationChoice = .none,
        language: AppLanguage = .english,
        acceptedSafetyReminder: Bool = false,
        status: ReportStatus = .draft,
        reportReference: String? = nil
    ) {
        self.id = id
        self.category = category
        self.description = description
        self.incidentTime = incidentTime
        self.location = location
        self.language = language
        self.acceptedSafetyReminder = acceptedSafetyReminder
        self.status = status
        self.reportReference = reportReference
    }
}
