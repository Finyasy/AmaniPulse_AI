import Foundation

public enum RiskLevel: String, CaseIterable, Codable, Identifiable, Sendable {
    case low
    case moderate
    case high
    case critical

    public var id: String { rawValue }
}

public struct RiskGuidance: Codable, Identifiable, Equatable, Sendable {
    public var id: String { countyCode }
    public let countyCode: String
    public let countyName: String
    public let level: RiskLevel
    public let summary: String
    public let guidance: [String]
    public let updatedAt: Date

    public init(
        countyCode: String,
        countyName: String,
        level: RiskLevel,
        summary: String,
        guidance: [String],
        updatedAt: Date = .now
    ) {
        self.countyCode = countyCode
        self.countyName = countyName
        self.level = level
        self.summary = summary
        self.guidance = guidance
        self.updatedAt = updatedAt
    }
}
