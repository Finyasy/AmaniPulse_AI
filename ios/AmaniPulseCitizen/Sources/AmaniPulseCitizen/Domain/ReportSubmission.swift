import Foundation

public struct ReportSubmissionPayload: Codable, Equatable, Sendable {
    public let clientReportId: UUID
    public let category: IncidentCategory
    public let description: String
    public let incidentTime: Date
    public let location: LocationChoice
    public let language: AppLanguage
    public let source: String
    public let appVersion: String
    public let consents: ReportConsents

    public init(
        clientReportId: UUID,
        category: IncidentCategory,
        description: String,
        incidentTime: Date,
        location: LocationChoice,
        language: AppLanguage,
        source: String = "ios_citizen_app",
        appVersion: String = "1.0.0",
        consents: ReportConsents = ReportConsents()
    ) {
        self.clientReportId = clientReportId
        self.category = category
        self.description = description
        self.incidentTime = incidentTime
        self.location = location
        self.language = language
        self.source = source
        self.appVersion = appVersion
        self.consents = consents
    }

    enum CodingKeys: String, CodingKey {
        case clientReportId = "client_report_id"
        case category
        case description
        case incidentTime = "incident_time"
        case location
        case language
        case source
        case appVersion = "app_version"
        case consents
    }
}

public struct ReportConsents: Codable, Equatable, Sendable {
    public let anonymousSubmission: Bool
    public let riskAnalysis: Bool

    public init(anonymousSubmission: Bool = true, riskAnalysis: Bool = true) {
        self.anonymousSubmission = anonymousSubmission
        self.riskAnalysis = riskAnalysis
    }

    enum CodingKeys: String, CodingKey {
        case anonymousSubmission = "anonymous_submission"
        case riskAnalysis = "risk_analysis"
    }
}

public struct ReportSubmissionResponse: Codable, Equatable, Sendable {
    public let reportReference: String
    public let status: ReportStatus
    public let receivedAt: Date
    public let message: String

    public init(reportReference: String, status: ReportStatus, receivedAt: Date, message: String) {
        self.reportReference = reportReference
        self.status = status
        self.receivedAt = receivedAt
        self.message = message
    }

    enum CodingKeys: String, CodingKey {
        case reportReference = "report_reference"
        case status
        case receivedAt = "received_at"
        case message
    }
}

public extension ReportDraft {
    func submissionPayload(appVersion: String = "1.0.0") -> ReportSubmissionPayload? {
        guard let category else {
            return nil
        }

        return ReportSubmissionPayload(
            clientReportId: id,
            category: category,
            description: description.trimmingCharacters(in: .whitespacesAndNewlines),
            incidentTime: incidentTime,
            location: location,
            language: language,
            appVersion: appVersion
        )
    }
}
