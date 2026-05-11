import XCTest
@testable import AmaniPulseCitizen

final class ReportDraftStoreTests: XCTestCase {
    func testInMemoryDraftStoreSavesLoadsAndDeletesDrafts() async throws {
        let store = InMemoryReportDraftStore()
        let draft = ReportDraft(
            category: .violenceThreat,
            description: "There are threats being shared near a rally.",
            acceptedSafetyReminder: true
        )

        try await store.save(draft)
        var drafts = try await store.loadDrafts()

        XCTAssertEqual(drafts, [draft])

        try await store.delete(draft)
        drafts = try await store.loadDrafts()

        XCTAssertTrue(drafts.isEmpty)
    }
}
