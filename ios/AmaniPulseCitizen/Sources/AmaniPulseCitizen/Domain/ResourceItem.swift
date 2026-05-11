import Foundation

public enum ResourceCategory: String, Codable, Sendable {
    case safetyPlanning = "safety_planning"
    case digitalSafety = "digital_safety"
    case rumorVerification = "rumor_verification"
    case partnerSupport = "partner_support"
}

public struct ResourceItem: Codable, Identifiable, Equatable, Sendable {
    public let id: String
    public let title: String
    public let body: String
    public let category: ResourceCategory

    public init(id: String, title: String, body: String, category: ResourceCategory) {
        self.id = id
        self.title = title
        self.body = body
        self.category = category
    }
}
