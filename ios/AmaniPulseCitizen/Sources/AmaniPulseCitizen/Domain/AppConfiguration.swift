import Foundation

public struct AppConfiguration: Codable, Equatable, Sendable {
    public let minimumSupportedVersion: String
    public let featureFlags: FeatureFlags
    public let emergencyDisclaimer: String
    public let supportChannels: SupportChannels

    public init(
        minimumSupportedVersion: String,
        featureFlags: FeatureFlags,
        emergencyDisclaimer: String,
        supportChannels: SupportChannels
    ) {
        self.minimumSupportedVersion = minimumSupportedVersion
        self.featureFlags = featureFlags
        self.emergencyDisclaimer = emergencyDisclaimer
        self.supportChannels = supportChannels
    }

    enum CodingKeys: String, CodingKey {
        case minimumSupportedVersion = "minimum_supported_version"
        case featureFlags = "feature_flags"
        case emergencyDisclaimer = "emergency_disclaimer"
        case supportChannels = "support_channels"
    }
}

public struct FeatureFlags: Codable, Equatable, Sendable {
    public let mediaUploads: Bool
    public let pushNotifications: Bool
    public let reportStatusLookup: Bool

    public init(mediaUploads: Bool, pushNotifications: Bool, reportStatusLookup: Bool) {
        self.mediaUploads = mediaUploads
        self.pushNotifications = pushNotifications
        self.reportStatusLookup = reportStatusLookup
    }

    enum CodingKeys: String, CodingKey {
        case mediaUploads = "media_uploads"
        case pushNotifications = "push_notifications"
        case reportStatusLookup = "report_status_lookup"
    }
}

public struct SupportChannels: Codable, Equatable, Sendable {
    public let sms: String?
    public let ussd: String?
    public let whatsapp: String?

    public init(sms: String?, ussd: String?, whatsapp: String?) {
        self.sms = sms
        self.ussd = ussd
        self.whatsapp = whatsapp
    }
}

public struct ReportStatusResponse: Codable, Equatable, Sendable {
    public let reportReference: String
    public let status: ReportStatus
    public let updatedAt: Date
    public let displayMessage: String

    public init(reportReference: String, status: ReportStatus, updatedAt: Date, displayMessage: String) {
        self.reportReference = reportReference
        self.status = status
        self.updatedAt = updatedAt
        self.displayMessage = displayMessage
    }

    enum CodingKeys: String, CodingKey {
        case reportReference = "report_reference"
        case status
        case updatedAt = "updated_at"
        case displayMessage = "display_message"
    }
}
