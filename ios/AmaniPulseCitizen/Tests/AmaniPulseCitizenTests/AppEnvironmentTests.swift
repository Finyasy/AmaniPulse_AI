import XCTest
@testable import AmaniPulseCitizen

final class AppEnvironmentTests: XCTestCase {
    func testDefaultEnvironmentUsesMockServices() {
        let environment = AppEnvironment.resolve(environment: [:], bundleAPIBaseURL: nil)

        XCTAssertEqual(environment, .mock)
    }

    func testLegacyRemoteFlagUsesLocalAPIProfile() throws {
        let environment = AppEnvironment.resolve(
            environment: ["AMANIPULSE_USE_REMOTE_API": "1"],
            bundleAPIBaseURL: nil
        )

        XCTAssertEqual(
            environment,
            .remote(profile: .local, baseURL: try XCTUnwrap(URL(string: "http://127.0.0.1:8000")))
        )
    }

    func testStagingProfileCanUseAcceleratorProvidedBaseURL() throws {
        let environment = AppEnvironment.resolve(
            environment: [
                "AMANIPULSE_API_PROFILE": "staging",
                "AMANIPULSE_API_BASE_URL": "https://accelerator-staging.amanipulse.test"
            ],
            bundleAPIBaseURL: nil
        )

        XCTAssertEqual(
            environment,
            .remote(
                profile: .staging,
                baseURL: try XCTUnwrap(URL(string: "https://accelerator-staging.amanipulse.test"))
            )
        )
    }

    func testBundleBaseURLIsUsedWhenEnvironmentDoesNotOverrideIt() throws {
        let environment = AppEnvironment.resolve(
            environment: ["AMANIPULSE_API_PROFILE": "production"],
            bundleAPIBaseURL: "https://api.amanipulse.example"
        )

        XCTAssertEqual(
            environment,
            .remote(profile: .production, baseURL: try XCTUnwrap(URL(string: "https://api.amanipulse.example")))
        )
    }

    func testBundleProfileAllowsDebugBuildToUseLocalBackendWhenTappedFromSimulator() throws {
        let environment = AppEnvironment.resolve(
            environment: [:],
            bundleAPIProfile: "local",
            bundleAPIBaseURL: "http://127.0.0.1:8000"
        )

        XCTAssertEqual(
            environment,
            .remote(profile: .local, baseURL: try XCTUnwrap(URL(string: "http://127.0.0.1:8000")))
        )
    }

    func testEnvironmentProfileOverridesBundleProfile() throws {
        let environment = AppEnvironment.resolve(
            environment: [
                "AMANIPULSE_API_PROFILE": "staging",
                "AMANIPULSE_API_BASE_URL": "https://accelerator-staging.amanipulse.test"
            ],
            bundleAPIProfile: "local",
            bundleAPIBaseURL: "http://127.0.0.1:8000"
        )

        XCTAssertEqual(
            environment,
            .remote(
                profile: .staging,
                baseURL: try XCTUnwrap(URL(string: "https://accelerator-staging.amanipulse.test"))
            )
        )
    }

    func testInvalidRemoteURLFallsBackToMock() {
        let environment = AppEnvironment.resolve(
            environment: [
                "AMANIPULSE_API_PROFILE": "staging",
                "AMANIPULSE_API_BASE_URL": "not a valid url"
            ],
            bundleAPIBaseURL: nil
        )

        XCTAssertEqual(environment, .mock)
    }
}
