import XCTest
@testable import AmaniPulseCitizen

final class APIClientTests: XCTestCase {
    override func tearDown() {
        MockURLProtocol.responseProvider = nil
        super.tearDown()
    }

    func testAppConfigurationUsesDocumentedQueryShape() async throws {
        let client = makeClient { request in
            XCTAssertEqual(request.url?.path, "/v1/app-config")
            XCTAssertTrue(request.url?.query?.contains("platform=ios") == true)
            XCTAssertTrue(request.url?.query?.contains("version=1.0.0") == true)
            XCTAssertTrue(request.url?.query?.contains("language=en") == true)

            return """
            {
              "minimum_supported_version": "1.0.0",
              "feature_flags": {
                "media_uploads": false,
                "push_notifications": false,
                "report_status_lookup": true
              },
              "emergency_disclaimer": "AmaniPulse is not an emergency response service.",
              "support_channels": {
                "sms": "TBD",
                "ussd": "TBD",
                "whatsapp": "TBD"
              }
            }
            """.data(using: .utf8)!
        }

        let configuration = try await client.appConfiguration(language: .english)

        XCTAssertEqual(configuration.minimumSupportedVersion, "1.0.0")
        XCTAssertTrue(configuration.featureFlags.reportStatusLookup)
        XCTAssertFalse(configuration.featureFlags.mediaUploads)
    }

    func testReportStatusDecodesUnderReviewStatus() async throws {
        let client = makeClient { request in
            XCTAssertEqual(request.url?.path, "/v1/reports/AP-2027-8F3KQ2/status")

            return """
            {
              "report_reference": "AP-2027-8F3KQ2",
              "status": "under_review",
              "updated_at": "2026-05-09T09:10:00Z",
              "display_message": "Your report has been received and is being reviewed."
            }
            """.data(using: .utf8)!
        }

        let status = try await client.reportStatus(reference: "AP-2027-8F3KQ2")

        XCTAssertEqual(status.reportReference, "AP-2027-8F3KQ2")
        XCTAssertEqual(status.status, .underReview)
    }

    private func makeClient(responseProvider: @escaping (URLRequest) throws -> Data) -> AmaniPulseAPIClient {
        MockURLProtocol.responseProvider = responseProvider
        let configuration = URLSessionConfiguration.ephemeral
        configuration.protocolClasses = [MockURLProtocol.self]
        return AmaniPulseAPIClient(
            baseURL: URL(string: "https://api.example.test")!,
            session: URLSession(configuration: configuration)
        )
    }
}

private final class MockURLProtocol: URLProtocol {
    nonisolated(unsafe) static var responseProvider: ((URLRequest) throws -> Data)?

    override class func canInit(with request: URLRequest) -> Bool {
        true
    }

    override class func canonicalRequest(for request: URLRequest) -> URLRequest {
        request
    }

    override func startLoading() {
        do {
            let data = try Self.responseProvider?(request) ?? Data()
            let response = HTTPURLResponse(
                url: request.url!,
                statusCode: 200,
                httpVersion: nil,
                headerFields: ["Content-Type": "application/json"]
            )!
            client?.urlProtocol(self, didReceive: response, cacheStoragePolicy: .notAllowed)
            client?.urlProtocol(self, didLoad: data)
            client?.urlProtocolDidFinishLoading(self)
        } catch {
            client?.urlProtocol(self, didFailWithError: error)
        }
    }

    override func stopLoading() {}
}
