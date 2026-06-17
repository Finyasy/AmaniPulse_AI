import Foundation

public protocol ReportDraftStoring: Sendable {
    func loadDrafts() async throws -> [ReportDraft]
    func save(_ draft: ReportDraft) async throws
    func delete(_ draft: ReportDraft) async throws
}

public actor InMemoryReportDraftStore: ReportDraftStoring {
    private var drafts: [UUID: ReportDraft] = [:]

    public init(seedDrafts: [ReportDraft] = []) {
        self.drafts = Dictionary(uniqueKeysWithValues: seedDrafts.map { ($0.id, $0) })
    }

    public func loadDrafts() async throws -> [ReportDraft] {
        drafts.values.sorted { $0.incidentTime > $1.incidentTime }
    }

    public func save(_ draft: ReportDraft) async throws {
        drafts[draft.id] = draft
    }

    public func delete(_ draft: ReportDraft) async throws {
        drafts.removeValue(forKey: draft.id)
    }
}
