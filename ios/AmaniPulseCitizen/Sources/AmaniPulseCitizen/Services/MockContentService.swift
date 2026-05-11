import Foundation

public protocol ContentProviding: Sendable {
    func resources(language: AppLanguage) async -> [ResourceItem]
    func riskGuidance(language: AppLanguage) async -> [RiskGuidance]
}

public struct MockContentService: ContentProviding {
    public init() {}

    public func resources(language: AppLanguage) async -> [ResourceItem] {
        switch language {
        case .english:
            [
                ResourceItem(
                    id: "move-to-safety",
                    title: "Move to safety first",
                    body: "If tension is rising, step away from crowds and report only when it is safe.",
                    category: .safetyPlanning
                ),
                ResourceItem(
                    id: "verify-rumors",
                    title: "Slow down rumors",
                    body: "Before forwarding a claim, check whether it comes from a trusted source.",
                    category: .rumorVerification
                ),
                ResourceItem(
                    id: "digital-safety",
                    title: "Protect your device",
                    body: "Use a passcode and avoid sharing screenshots that could identify someone.",
                    category: .digitalSafety
                )
            ]
        case .swahili:
            [
                ResourceItem(
                    id: "move-to-safety",
                    title: "Kwanza nenda mahali salama",
                    body: "Mvutano ukiongezeka, ondoka kwenye umati na uripoti tu ukiwa salama.",
                    category: .safetyPlanning
                ),
                ResourceItem(
                    id: "verify-rumors",
                    title: "Punguza uvumi",
                    body: "Kabla ya kusambaza dai, hakikisha limetoka kwa chanzo kinachoaminika.",
                    category: .rumorVerification
                ),
                ResourceItem(
                    id: "digital-safety",
                    title: "Linda kifaa chako",
                    body: "Tumia nenosiri na epuka kusambaza picha zinazoweza kumtambulisha mtu.",
                    category: .digitalSafety
                )
            ]
        }
    }

    public func riskGuidance(language: AppLanguage) async -> [RiskGuidance] {
        switch language {
        case .english:
            [
                RiskGuidance(
                    countyCode: "KE-30",
                    countyName: "Nairobi",
                    level: .moderate,
                    summary: "Community reports suggest elevated tension in some areas.",
                    guidance: [
                        "Avoid sharing unverified claims.",
                        "Move away from crowds if tensions rise.",
                        "Use anonymous reporting if you witness intimidation."
                    ]
                ),
                RiskGuidance(
                    countyCode: "KE-17",
                    countyName: "Mombasa",
                    level: .low,
                    summary: "No broad escalation signal is available right now.",
                    guidance: [
                        "Keep checking trusted updates.",
                        "Report early signs if you can do so safely."
                    ]
                )
            ]
        case .swahili:
            [
                RiskGuidance(
                    countyCode: "KE-30",
                    countyName: "Nairobi",
                    level: .moderate,
                    summary: "Ripoti za jamii zinaonyesha mvutano umeongezeka katika baadhi ya maeneo.",
                    guidance: [
                        "Epuka kusambaza taarifa ambazo hujathibitisha.",
                        "Ondoka kwenye umati mvutano ukiongezeka.",
                        "Tumia ripoti ya siri ukiona vitisho."
                    ]
                ),
                RiskGuidance(
                    countyCode: "KE-17",
                    countyName: "Mombasa",
                    level: .low,
                    summary: "Hakuna ishara pana ya kuongezeka kwa hatari kwa sasa.",
                    guidance: [
                        "Endelea kufuatilia taarifa zinazoaminika.",
                        "Ripoti dalili za mapema ikiwa unaweza kufanya hivyo kwa usalama."
                    ]
                )
            ]
        }
    }
}
