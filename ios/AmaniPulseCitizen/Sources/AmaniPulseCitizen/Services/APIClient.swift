import Foundation

public enum APIClientError: Error, Equatable, Sendable {
    case invalidResponse
    case server(code: String, message: String, retryable: Bool)
}

public protocol ReportSubmitting: Sendable {
    func submit(_ payload: ReportSubmissionPayload) async throws -> ReportSubmissionResponse
    func reportStatus(reference: String) async throws -> ReportStatusResponse
}

public protocol RemoteContentProviding: ContentProviding {
    func incidentTaxonomy(language: AppLanguage) async throws -> [IncidentCategory]
    func appConfiguration(platform: String, version: String, language: AppLanguage) async throws -> AppConfiguration
}

public struct AmaniPulseAPIClient: ReportSubmitting, RemoteContentProviding {
    private let baseURL: URL
    private let session: URLSession
    private let decoder: JSONDecoder
    private let encoder: JSONEncoder

    public init(baseURL: URL, session: URLSession = .shared) {
        self.baseURL = baseURL
        self.session = session

        let decoder = JSONDecoder()
        decoder.dateDecodingStrategy = .iso8601
        self.decoder = decoder

        let encoder = JSONEncoder()
        encoder.dateEncodingStrategy = .iso8601
        encoder.keyEncodingStrategy = .useDefaultKeys
        self.encoder = encoder
    }

    public func submit(_ payload: ReportSubmissionPayload) async throws -> ReportSubmissionResponse {
        var request = URLRequest(url: baseURL.appending(path: "v1/reports"))
        request.httpMethod = "POST"
        request.setValue("application/json", forHTTPHeaderField: "Content-Type")
        request.httpBody = try encoder.encode(payload)

        return try await perform(request)
    }

    public func reportStatus(reference: String) async throws -> ReportStatusResponse {
        let encodedReference = reference.addingPercentEncoding(withAllowedCharacters: .urlPathAllowed) ?? reference
        let request = URLRequest(url: baseURL.appending(path: "v1/reports/\(encodedReference)/status"))
        return try await perform(request)
    }

    public func incidentTaxonomy(language: AppLanguage) async throws -> [IncidentCategory] {
        var components = URLComponents(url: baseURL.appending(path: "v1/incident-taxonomy"), resolvingAgainstBaseURL: false)
        components?.queryItems = [URLQueryItem(name: "language", value: language.rawValue)]

        guard let url = components?.url else {
            throw APIClientError.invalidResponse
        }

        let response: IncidentTaxonomyResponse = try await perform(URLRequest(url: url))
        return response.categories.compactMap { IncidentCategory(rawValue: $0.id) }
    }

    public func appConfiguration(
        platform: String = "ios",
        version: String = "1.0.0",
        language: AppLanguage
    ) async throws -> AppConfiguration {
        var components = URLComponents(url: baseURL.appending(path: "v1/app-config"), resolvingAgainstBaseURL: false)
        components?.queryItems = [
            URLQueryItem(name: "platform", value: platform),
            URLQueryItem(name: "version", value: version),
            URLQueryItem(name: "language", value: language.rawValue)
        ]

        guard let url = components?.url else {
            throw APIClientError.invalidResponse
        }

        return try await perform(URLRequest(url: url))
    }

    public func resources(language: AppLanguage) async -> [ResourceItem] {
        var components = URLComponents(url: baseURL.appending(path: "v1/resources"), resolvingAgainstBaseURL: false)
        components?.queryItems = [
            URLQueryItem(name: "language", value: language.rawValue),
            URLQueryItem(name: "country", value: "KE")
        ]

        guard let url = components?.url else {
            return []
        }

        do {
            let response: ResourcesResponse = try await perform(URLRequest(url: url))
            return response.resources.map(\.resourceItem)
        } catch {
            return []
        }
    }

    public func riskGuidance(language: AppLanguage) async -> [RiskGuidance] {
        let counties = ["KE-30", "KE-17"]

        return await withTaskGroup(of: RiskGuidance?.self) { group in
            for county in counties {
                group.addTask {
                    let url = baseURL.appending(path: "v1/risk/county/\(county)")
                    do {
                        let response: RiskGuidanceResponse = try await perform(URLRequest(url: url))
                        return response.riskGuidance
                    } catch {
                        return nil
                    }
                }
            }

            var guidance: [RiskGuidance] = []
            for await item in group {
                if let item {
                    guidance.append(item)
                }
            }
            return guidance.sorted { $0.countyName < $1.countyName }
        }
    }

    private func perform<T: Decodable>(_ request: URLRequest) async throws -> T {
        let (data, response) = try await session.data(for: request)
        guard let httpResponse = response as? HTTPURLResponse else {
            throw APIClientError.invalidResponse
        }

        if (200..<300).contains(httpResponse.statusCode) {
            return try decoder.decode(T.self, from: data)
        }

        if let errorResponse = try? decoder.decode(APIErrorResponse.self, from: data) {
            throw APIClientError.server(
                code: errorResponse.error.code,
                message: errorResponse.error.message,
                retryable: errorResponse.error.retryable
            )
        }

        throw APIClientError.invalidResponse
    }
}

private struct IncidentTaxonomyResponse: Decodable {
    let categories: [IncidentCategoryResponse]
}

private struct IncidentCategoryResponse: Decodable {
    let id: String
}

private struct RiskGuidanceResponse: Decodable {
    let countyCode: String
    let countyName: String
    let riskLevel: RiskLevel
    let summary: String
    let guidance: [String]
    let updatedAt: Date

    var riskGuidance: RiskGuidance {
        RiskGuidance(
            countyCode: countyCode,
            countyName: countyName,
            level: riskLevel,
            summary: summary,
            guidance: guidance,
            updatedAt: updatedAt
        )
    }

    enum CodingKeys: String, CodingKey {
        case countyCode = "county_code"
        case countyName = "county_name"
        case riskLevel = "risk_level"
        case summary
        case guidance
        case updatedAt = "updated_at"
    }
}

private struct ResourcesResponse: Decodable {
    let resources: [ResourceResponse]
}

private struct ResourceResponse: Decodable {
    let id: String
    let title: String
    let body: String
    let category: ResourceCategory

    var resourceItem: ResourceItem {
        ResourceItem(id: id, title: title, body: body, category: category)
    }
}

private struct APIErrorResponse: Decodable {
    let error: APIErrorBody
}

private struct APIErrorBody: Decodable {
    let code: String
    let message: String
    let retryable: Bool
}
