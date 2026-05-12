import Foundation

public enum APIProfile: String, Equatable, Sendable {
    case mock
    case local
    case staging
    case production
}

public enum AppEnvironment: Equatable, Sendable {
    case mock
    case remote(profile: APIProfile, baseURL: URL)

    public static func current(
        processInfo: ProcessInfo = .processInfo,
        bundle: Bundle = .main
    ) -> AppEnvironment {
        resolve(
            environment: processInfo.environment,
            bundleAPIProfile: bundle.object(forInfoDictionaryKey: "AMANIPULSE_API_PROFILE") as? String,
            bundleAPIBaseURL: bundle.object(forInfoDictionaryKey: "AMANIPULSE_API_BASE_URL") as? String
        )
    }

    public static func resolve(
        environment: [String: String],
        bundleAPIProfile: String? = nil,
        bundleAPIBaseURL: String?
    ) -> AppEnvironment {
        let profileName = environment["AMANIPULSE_API_PROFILE"] ?? bundleAPIProfile ?? ""
        let profile = APIProfile(rawValue: profileName) ?? legacyProfile(from: environment)
        guard profile != .mock else {
            return .mock
        }

        let urlString = environment["AMANIPULSE_API_BASE_URL"] ?? bundleAPIBaseURL ?? defaultBaseURL(for: profile)

        guard let url = URL(string: urlString), isSupportedRemoteURL(url) else {
            return .mock
        }

        return .remote(profile: profile, baseURL: url)
    }

    private static func legacyProfile(from environment: [String: String]) -> APIProfile {
        if environment["AMANIPULSE_USE_REMOTE_API"] == "1" {
            return .local
        }

        return .mock
    }

    private static func defaultBaseURL(for profile: APIProfile) -> String {
        switch profile {
        case .mock:
            return "mock://local"
        case .local:
            return "http://127.0.0.1:8000"
        case .staging:
            return "https://staging-api.amanipulse.example"
        case .production:
            return "https://api.amanipulse.example"
        }
    }

    private static func isSupportedRemoteURL(_ url: URL) -> Bool {
        guard let scheme = url.scheme?.lowercased(), url.host != nil else {
            return false
        }

        return scheme == "http" || scheme == "https"
    }
}
