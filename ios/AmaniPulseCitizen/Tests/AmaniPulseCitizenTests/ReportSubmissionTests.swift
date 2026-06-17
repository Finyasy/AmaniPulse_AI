import XCTest
@testable import AmaniPulseCitizen

final class ReportSubmissionTests: XCTestCase {
    func testDraftCreatesBackendCompatibleSubmissionPayload() throws {
        let draft = ReportDraft(
            id: UUID(uuidString: "00000000-0000-0000-0000-000000000001")!,
            category: .voterIntimidation,
            description: " People are being warned not to attend registration. ",
            location: .manualArea(county: "Nairobi", areaLabel: "Kasarani"),
            language: .english,
            acceptedSafetyReminder: true
        )

        let payload = try XCTUnwrap(draft.submissionPayload(appVersion: "1.0.0"))

        XCTAssertEqual(payload.clientReportId, draft.id)
        XCTAssertEqual(payload.category, .voterIntimidation)
        XCTAssertEqual(payload.description, "People are being warned not to attend registration.")
        XCTAssertEqual(payload.location, .manualArea(county: "Nairobi", areaLabel: "Kasarani"))
        XCTAssertEqual(payload.source, "ios_citizen_app")
        XCTAssertTrue(payload.consents.anonymousSubmission)
        XCTAssertTrue(payload.consents.riskAnalysis)
    }

    func testReportStatusUsesBackendSnakeCaseValues() {
        XCTAssertEqual(ReportStatus.waitingForNetwork.rawValue, "waiting_for_network")
        XCTAssertEqual(ReportStatus.underReview.rawValue, "under_review")
        XCTAssertEqual(ReportStatus.unableToProcess.rawValue, "unable_to_process")
    }
}
