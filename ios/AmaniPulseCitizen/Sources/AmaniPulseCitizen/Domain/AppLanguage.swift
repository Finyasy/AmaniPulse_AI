import Foundation

public enum AppLanguage: String, CaseIterable, Codable, Identifiable, Sendable {
    case english = "en"
    case swahili = "sw"

    public var id: String { rawValue }

    public var displayName: String {
        switch self {
        case .english:
            "English"
        case .swahili:
            "Kiswahili"
        }
    }

    public static func preferred(from locale: Locale = .autoupdatingCurrent) -> AppLanguage {
        guard let languageCode = locale.language.languageCode?.identifier else {
            return .english
        }

        return AppLanguage(rawValue: languageCode) ?? .english
    }
}
