import XCTest
@testable import AmaniPulseCitizen

final class MockContentServiceTests: XCTestCase {
    func testMockContentProvidesOfflineResourcesAndRiskGuidance() async {
        let service = MockContentService()

        let resources = await service.resources(language: .english)
        let riskGuidance = await service.riskGuidance(language: .english)

        XCTAssertGreaterThanOrEqual(resources.count, 3)
        XCTAssertTrue(resources.contains { $0.category == .digitalSafety })
        XCTAssertTrue(riskGuidance.contains { $0.countyCode == "KE-30" })
    }
}
