import XCTest
@testable import AmaniPulseCitizen

@MainActor
final class AppViewModelTests: XCTestCase {
    func testOfflineSubmissionSavesDraftAsWaitingForNetwork() async throws {
        let store = InMemoryReportDraftStore()
        let model = AppViewModel(isNetworkAvailable: false, draftStore: store)
        let draft = ReportDraft(
            category: .voterIntimidation,
            description: "People are being warned not to attend registration.",
            acceptedSafetyReminder: true
        )

        let outcome = await model.submitDraft(draft)
        let savedDrafts = try await store.loadDrafts()

        XCTAssertEqual(outcome, .savedForNetwork)
        XCTAssertEqual(savedDrafts.count, 1)
        XCTAssertEqual(savedDrafts.first?.status, .waitingForNetwork)
    }

    func testSuccessfulSubmissionStoresLocalReferenceForStatusLookup() async throws {
        let store = InMemoryReportDraftStore()
        let submitter = StubReportSubmitter(submitStatus: .received, refreshedStatus: .underReview)
        let model = AppViewModel(draftStore: store, reportSubmitter: submitter)
        let draft = validDraft()

        let outcome = await model.submitDraft(draft)
        let savedDrafts = try await store.loadDrafts()

        XCTAssertEqual(outcome, .submitted(ReportSubmissionResponse(
            reportReference: "AP-TEST-001",
            status: .received,
            receivedAt: StubReportSubmitter.referenceDate,
            message: "Received"
        )))
        XCTAssertEqual(savedDrafts.first?.reportReference, "AP-TEST-001")
        XCTAssertEqual(savedDrafts.first?.status, .received)
    }

    func testRefreshStatusUpdatesSavedReport() async throws {
        let store = InMemoryReportDraftStore(seedDrafts: [
            validDraft(status: .received, reportReference: "AP-TEST-001")
        ])
        let submitter = StubReportSubmitter(submitStatus: .received, refreshedStatus: .underReview)
        let model = AppViewModel(draftStore: store, reportSubmitter: submitter)
        await model.refreshContent()

        await model.refreshStatus(for: try XCTUnwrap(model.savedDrafts.first))

        let savedDrafts = try await store.loadDrafts()
        XCTAssertEqual(savedDrafts.first?.status, .underReview)
    }

    func testRetryWaitingDraftsSubmitsSavedReportsWhenNetworkReturns() async throws {
        let store = InMemoryReportDraftStore(seedDrafts: [
            validDraft(status: .waitingForNetwork)
        ])
        let submitter = StubReportSubmitter(submitStatus: .received, refreshedStatus: .underReview)
        let model = AppViewModel(isNetworkAvailable: true, draftStore: store, reportSubmitter: submitter)
        await model.refreshContent()

        await model.retryWaitingDrafts()

        let savedDrafts = try await store.loadDrafts()
        XCTAssertEqual(savedDrafts.first?.status, .received)
        XCTAssertEqual(savedDrafts.first?.reportReference, "AP-TEST-001")
    }

    private func validDraft(
        status: ReportStatus = .draft,
        reportReference: String? = nil
    ) -> ReportDraft {
        ReportDraft(
            category: .voterIntimidation,
            description: "People are being warned not to attend registration.",
            acceptedSafetyReminder: true,
            status: status,
            reportReference: reportReference
        )
    }
}

private struct StubReportSubmitter: ReportSubmitting {
    static let referenceDate = Date(timeIntervalSince1970: 1_830_384_000)

    let submitStatus: ReportStatus
    let refreshedStatus: ReportStatus

    func submit(_ payload: ReportSubmissionPayload) async throws -> ReportSubmissionResponse {
        ReportSubmissionResponse(
            reportReference: "AP-TEST-001",
            status: submitStatus,
            receivedAt: Self.referenceDate,
            message: "Received"
        )
    }

    func reportStatus(reference: String) async throws -> ReportStatusResponse {
        ReportStatusResponse(
            reportReference: reference,
            status: refreshedStatus,
            updatedAt: Self.referenceDate,
            displayMessage: "Updated"
        )
    }
}
