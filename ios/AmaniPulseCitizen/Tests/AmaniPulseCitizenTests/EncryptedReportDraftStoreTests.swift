import XCTest
@testable import AmaniPulseCitizen

final class EncryptedReportDraftStoreTests: XCTestCase {
    func testEncryptedStorePersistsDraftsWithoutPlainText() async throws {
        let directory = URL(fileURLWithPath: NSTemporaryDirectory())
            .appending(path: UUID().uuidString, directoryHint: .isDirectory)
        let fileURL = directory.appending(path: "drafts.bin")
        let store = EncryptedReportDraftStore(
            fileURL: fileURL,
            keyProvider: EphemeralEncryptionKeyProvider()
        )
        let draft = ReportDraft(
            category: .hateSpeechOrIncitement,
            description: "Messages are encouraging harm toward a group.",
            acceptedSafetyReminder: true
        )

        try await store.save(draft)

        let storedData = try Data(contentsOf: fileURL)
        let storedText = String(data: storedData, encoding: .utf8) ?? ""
        let loadedDrafts = try await store.loadDrafts()

        XCTAssertFalse(storedText.contains(draft.description))
        XCTAssertEqual(loadedDrafts.count, 1)
        XCTAssertEqual(loadedDrafts.first?.id, draft.id)
        XCTAssertEqual(loadedDrafts.first?.description, draft.description)
        XCTAssertEqual(loadedDrafts.first?.category, draft.category)
    }
}
